import pytest
import pytest_asyncio
import os
from infra.db.mongodb.account_repository import AccountMongoRepository
from infra.db.mongodb.helpers.mongo_helper import MongoHelper


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    """Setup and teardown for MongoDB connection and clean database between tests."""
    mongo_url = os.getenv("MONGO_URL", "mongodb://flask_user:flask_password@localhost:27017")
    await MongoHelper.connect(mongo_url)
    
    # Clean up BEFORE the test: ensure clean state
    collection = MongoHelper.get_collection("accounts")
    collection.delete_many({})  # Delete all documents instead of dropping collection
    
    yield
    
    # Clean up AFTER the test
    collection.delete_many({})
    await MongoHelper.disconnect()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_should_return_an_account_on_success():
    sut = AccountMongoRepository()
    from domain.usecases.add_account import AddAccountModel
    
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