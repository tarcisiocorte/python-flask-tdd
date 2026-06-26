import pytest
import pytest_asyncio
import os
from pymongo.errors import OperationFailure

from data.usecases.add_account.db_add_account import DbAddAccount
from data.usecases.authentication import DbAuthentication
from domain.usecases import AuthenticationParams
from domain.usecases.add_account import AddAccountModel
from infra.cryptography import BcryptAdapter, JwtAdapter
from infra.db.mongodb.account_repository import AccountMongoRepository
from infra.db.mongodb.helpers.mongo_helper import MongoHelper


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    """Setup and teardown for MongoDB connection and clean database between tests."""
    mongo_url = os.getenv("MONGO_URL")
    if not mongo_url:
        pytest.skip(
            "MONGO_URL is required for MongoDB integration tests. "
            "Use make test-integration or set an authenticated MongoDB URI."
        )

    try:
        await MongoHelper.connect(mongo_url)
    except OperationFailure as exc:
        if exc.code == 18:
            pytest.fail(
                "MongoDB authentication failed. If the Docker volume was created "
                "with old credentials, recreate it with: "
                "docker-compose down -v && docker-compose up -d mongodb"
            )
        raise

    collection = MongoHelper.get_collection("accounts")
    collection.delete_many({})

    yield

    collection.delete_many({})
    await MongoHelper.disconnect()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_should_return_an_account_on_success():
    sut = AccountMongoRepository()
    
    account = await sut.add(AddAccountModel(
        name="any_name",
        email="any_email@mail.com",
        password="any_password"
    ))
    
    assert account is not None
    assert account.id is not None
    assert account.name == "any_name"
    assert account.email == "any_email@mail.com"
    assert account.password == "any_password"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_check_by_email_returns_false_before_insert_and_true_after_insert():
    sut = AccountMongoRepository()

    exists_before_insert = await sut.check_by_email("any_email@mail.com")
    await sut.add(AddAccountModel(
        name="any_name",
        email="any_email@mail.com",
        password="any_password"
    ))
    exists_after_insert = await sut.check_by_email("any_email@mail.com")

    assert exists_before_insert is False
    assert exists_after_insert is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_load_by_email_returns_account_with_password_role_and_token():
    sut = AccountMongoRepository()
    collection = MongoHelper.get_collection("accounts")
    account_id = collection.insert_one({
        "name": "any_name",
        "email": "any_email@mail.com",
        "password": "hashed_password",
        "accessToken": "stored_token",
        "role": "admin",
    }).inserted_id

    account = await sut.load_by_email("any_email@mail.com")

    assert account.id == str(account_id)
    assert account.name == "any_name"
    assert account.email == "any_email@mail.com"
    assert account.password == "hashed_password"
    assert account.access_token == "stored_token"
    assert account.role == "admin"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_update_access_token_stores_token_as_access_token():
    sut = AccountMongoRepository()
    account_id = MongoHelper.get_collection("accounts").insert_one({
        "name": "any_name",
        "email": "any_email@mail.com",
        "password": "hashed_password",
    }).inserted_id

    await sut.update_access_token(str(account_id), "new_token")

    stored_account = MongoHelper.get_collection("accounts").find_one(
        {"_id": account_id}
    )
    assert stored_account["accessToken"] == "new_token"
    assert "access_token" not in stored_account


@pytest.mark.integration
@pytest.mark.asyncio
async def test_load_by_token_returns_account_by_token():
    sut = AccountMongoRepository()
    account_id = MongoHelper.get_collection("accounts").insert_one({
        "name": "any_name",
        "email": "any_email@mail.com",
        "password": "hashed_password",
        "accessToken": "stored_token",
    }).inserted_id

    account = await sut.load_by_token("stored_token")

    assert account.id == str(account_id)
    assert account.name == "any_name"
    assert account.access_token == "stored_token"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_load_by_token_with_admin_role_allows_admin_and_rejects_non_admin():
    sut = AccountMongoRepository()
    collection = MongoHelper.get_collection("accounts")
    admin_id = collection.insert_one({
        "name": "admin_name",
        "email": "admin@mail.com",
        "password": "hashed_password",
        "accessToken": "admin_token",
        "role": "admin",
    }).inserted_id
    collection.insert_one({
        "name": "user_name",
        "email": "user@mail.com",
        "password": "hashed_password",
        "accessToken": "user_token",
        "role": "user",
    })

    admin_account = await sut.load_by_token("admin_token", "admin")
    user_account = await sut.load_by_token("user_token", "admin")

    assert admin_account.id == str(admin_id)
    assert admin_account.role == "admin"
    assert user_account is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_db_add_account_persists_hashed_password_and_checks_duplicate_email():
    repository = AccountMongoRepository()
    bcrypt_adapter = BcryptAdapter(4)
    sut = DbAddAccount(bcrypt_adapter, repository, repository)

    account = await sut.add(AddAccountModel(
        name="any_name",
        email="any_email@mail.com",
        password="Valid_password123"
    ))

    collection = MongoHelper.get_collection("accounts")
    stored_account = collection.find_one({"email": "any_email@mail.com"})

    assert account is not None
    assert stored_account["password"] != "Valid_password123"
    assert await bcrypt_adapter.compare("Valid_password123", stored_account["password"])
    assert await repository.check_by_email("any_email@mail.com") is True

    duplicated_account = await sut.add(AddAccountModel(
        name="any_name",
        email="any_email@mail.com",
        password="Other_password123"
    ))

    assert duplicated_account is None
    assert collection.count_documents({"email": "any_email@mail.com"}) == 1


@pytest.mark.integration
@pytest.mark.asyncio
async def test_signup_authentication_generates_and_persists_access_token():
    repository = AccountMongoRepository()
    bcrypt_adapter = BcryptAdapter(4)
    jwt_adapter = JwtAdapter("test-secret-that-is-long-enough-for-hs256")
    add_account = DbAddAccount(bcrypt_adapter, repository, repository)
    authentication = DbAuthentication(
        repository,
        bcrypt_adapter,
        jwt_adapter,
        repository,
    )

    account = await add_account.add(AddAccountModel(
        name="any_name",
        email="any_email@mail.com",
        password="Valid_password123"
    ))
    auth_model = await authentication.auth(AuthenticationParams(
        email="any_email@mail.com",
        password="Valid_password123",
    ))

    stored_account = MongoHelper.get_collection("accounts").find_one(
        {"email": "any_email@mail.com"}
    )

    assert auth_model is not None
    assert auth_model.access_token == stored_account["accessToken"]
    assert await jwt_adapter.decrypt(auth_model.access_token) == account.id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_login_authentication_replaces_stored_access_token():
    repository = AccountMongoRepository()
    bcrypt_adapter = BcryptAdapter(4)
    jwt_adapter = JwtAdapter("test-secret-that-is-long-enough-for-hs256")
    add_account = DbAddAccount(bcrypt_adapter, repository, repository)
    authentication = DbAuthentication(
        repository,
        bcrypt_adapter,
        jwt_adapter,
        repository,
    )

    account = await add_account.add(AddAccountModel(
        name="any_name",
        email="any_email@mail.com",
        password="Valid_password123"
    ))
    await repository.update_access_token(account.id, "old_token")

    auth_model = await authentication.auth(AuthenticationParams(
        email="any_email@mail.com",
        password="Valid_password123",
    ))
    stored_account = MongoHelper.get_collection("accounts").find_one(
        {"email": "any_email@mail.com"}
    )

    assert auth_model is not None
    assert stored_account["accessToken"] == auth_model.access_token
    assert stored_account["accessToken"] != "old_token"
