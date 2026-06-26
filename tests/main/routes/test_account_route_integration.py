import asyncio
from copy import deepcopy
from types import SimpleNamespace

import pytest
from bson import ObjectId

from infra.cryptography import BcryptAdapter
from infra.db.mongodb.helpers.mongo_helper import MongoHelper
from main.config.app import create_app
from main.config.env import jwt_secret


PUBLIC_AUTH_FIELDS = {"accessToken", "name"}
PRIVATE_AUTH_FIELDS = {"access_token", "password", "email", "id"}


class FakeCollection:
    def __init__(self):
        self.documents = []

    def delete_many(self, query):
        if not query:
            self.documents.clear()
            return
        self.documents = [
            document for document in self.documents if not self._matches(document, query)
        ]

    def insert_one(self, document):
        stored_document = deepcopy(document)
        stored_document["_id"] = ObjectId()
        self.documents.append(stored_document)
        return SimpleNamespace(inserted_id=stored_document["_id"])

    def find_one(self, query, projection=None):
        for document in self.documents:
            if self._matches(document, query):
                return deepcopy(document)
        return None

    def update_one(self, query, update):
        for document in self.documents:
            if self._matches(document, query):
                document.update(update.get("$set", {}))
                return

    def count_documents(self, query):
        return sum(1 for document in self.documents if self._matches(document, query))

    def _matches(self, document, query):
        for key, expected_value in query.items():
            if key == "$or":
                if not any(self._matches(document, option) for option in expected_value):
                    return False
                continue
            if document.get(key) != expected_value:
                return False
        return True


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("ENV", "test")
    monkeypatch.setenv("JWT_SECRET", "test-secret-that-is-long-enough-for-hs256")
    monkeypatch.setenv("BCRYPT_SALT", "4")
    monkeypatch.setenv("AUTH_RATE_LIMIT_MAX_REQUESTS", "100")
    monkeypatch.setenv("MONGO_DB_NAME", "flask_tdd_route_test")
    jwt_secret.cache_clear()
    collection = FakeCollection()
    monkeypatch.setattr(
        MongoHelper,
        "get_collection",
        lambda collection_name, db_name=None: collection,
    )

    app = create_app()
    app.config["TESTING"] = True

    yield app.test_client()

    collection.delete_many({})
    jwt_secret.cache_clear()


def assert_public_auth_body(body, name):
    assert set(body) == PUBLIC_AUTH_FIELDS
    assert PRIVATE_AUTH_FIELDS.isdisjoint(body)
    assert isinstance(body["accessToken"], str)
    assert body["accessToken"]
    assert body["name"] == name


@pytest.mark.parametrize(
    "field",
    ["name", "email", "password", "passwordConfirmation"],
)
def test_signup_route_returns_400_for_missing_required_fields(client, field):
    payload = {
        "name": "Ada",
        "email": "ada@example.com",
        "password": "Valid_password123",
        "passwordConfirmation": "Valid_password123",
    }
    payload.pop(field)

    response = client.post("/api/signup", json=payload)

    assert response.status_code == 400
    assert response.get_json() == {"error": f"Missing param: {field}"}


def test_signup_route_returns_400_for_invalid_email(client):
    response = client.post("/api/signup", json={
        "name": "Ada",
        "email": "invalid_email",
        "password": "Valid_password123",
        "passwordConfirmation": "Valid_password123",
    })

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid param: email"}


def test_signup_route_returns_400_for_password_mismatch(client):
    response = client.post("/api/signup", json={
        "name": "Ada",
        "email": "ada@example.com",
        "password": "Valid_password123",
        "passwordConfirmation": "Other_password123",
    })

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid param: passwordConfirmation"}


def test_signup_route_returns_403_for_duplicate_email(client):
    payload = {
        "name": "Ada",
        "email": "ada@example.com",
        "password": "Valid_password123",
        "passwordConfirmation": "Valid_password123",
    }

    first_response = client.post("/api/signup", json=payload)
    second_response = client.post("/api/signup", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 403
    assert second_response.get_json() == {"error": "Email already in use"}


def test_signup_route_success_returns_public_body_and_stores_hash_and_token(client):
    response = client.post("/api/signup", json={
        "name": "Ada",
        "email": "ada@example.com",
        "password": "Valid_password123",
        "passwordConfirmation": "Valid_password123",
    })

    body = response.get_json()
    stored_account = MongoHelper.get_collection("accounts").find_one(
        {"email": "ada@example.com"}
    )
    bcrypt_adapter = BcryptAdapter(4)

    assert response.status_code == 200
    assert_public_auth_body(body, "Ada")
    assert stored_account["password"] != "Valid_password123"
    assert asyncio.run(
        bcrypt_adapter.compare("Valid_password123", stored_account["password"])
    )
    assert stored_account["accessToken"] == body["accessToken"]


@pytest.mark.parametrize(
    "payload, error",
    [
        ({"password": "Valid_password123"}, "Missing param: email"),
        ({"email": "ada@example.com"}, "Missing param: password"),
        (
            {"email": "invalid_email", "password": "Valid_password123"},
            "Invalid param: email",
        ),
    ],
)
def test_login_route_returns_400_for_invalid_request(client, payload, error):
    response = client.post("/api/login", json=payload)

    assert response.status_code == 400
    assert response.get_json() == {"error": error}


def test_login_route_returns_401_for_unknown_email(client):
    response = client.post("/api/login", json={
        "email": "unknown@example.com",
        "password": "Valid_password123",
    })

    assert response.status_code == 401
    assert response.get_json() == {"error": "Unauthorized"}


def test_login_route_returns_401_for_wrong_password(client):
    client.post("/api/signup", json={
        "name": "Ada",
        "email": "ada@example.com",
        "password": "Valid_password123",
        "passwordConfirmation": "Valid_password123",
    })

    response = client.post("/api/login", json={
        "email": "ada@example.com",
        "password": "Wrong_password123",
    })

    assert response.status_code == 401
    assert response.get_json() == {"error": "Unauthorized"}


def test_login_route_success_returns_public_body_and_updates_stored_token(client):
    client.post("/api/signup", json={
        "name": "Ada",
        "email": "ada@example.com",
        "password": "Valid_password123",
        "passwordConfirmation": "Valid_password123",
    })
    collection = MongoHelper.get_collection("accounts")
    collection.update_one(
        {"email": "ada@example.com"},
        {"$set": {"accessToken": "old_token"}},
    )

    response = client.post("/api/login", json={
        "email": "ada@example.com",
        "password": "Valid_password123",
    })

    body = response.get_json()
    stored_account = collection.find_one({"email": "ada@example.com"})

    assert response.status_code == 200
    assert_public_auth_body(body, "Ada")
    assert stored_account["accessToken"] == body["accessToken"]
    assert stored_account["accessToken"] != "old_token"
