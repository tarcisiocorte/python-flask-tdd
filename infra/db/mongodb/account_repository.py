from __future__ import annotations

"""MongoDB Account Repository implementation."""
from bson import ObjectId

from data.protocols.add_account_repository import (
    AddAccountRepository,
    CheckAccountByEmailRepository,
    LoadAccountByEmailRepository,
    LoadAccountByTokenRepository,
    UpdateAccessTokenRepository,
)
from domain.usecases.add_account import AddAccountModel
from domain.models.account import AccountModel
from infra.db.mongodb.helpers.mongo_helper import MongoHelper


class AccountMongoRepository(
    AddAccountRepository,
    CheckAccountByEmailRepository,
    LoadAccountByEmailRepository,
    LoadAccountByTokenRepository,
    UpdateAccessTokenRepository,
):
    """MongoDB implementation of AddAccountRepository."""

    async def add(self, account_data: AddAccountModel) -> AccountModel:
        collection = MongoHelper.get_collection("accounts")
        account_dict = {
            "name": account_data.name,
            "email": account_data.email,
            "password": account_data.password
        }
        result = collection.insert_one(account_dict)
        return AccountModel(
            id=str(result.inserted_id),
            name=account_data.name,
            email=account_data.email,
            password=account_data.password,
        )

    async def load_by_email(self, email: str) -> AccountModel | None:
        collection = MongoHelper.get_collection("accounts")
        account = collection.find_one(
            {"email": email},
            {"_id": 1, "name": 1, "email": 1, "password": 1, "accessToken": 1, "role": 1},
        )
        return self._to_model(account) if account else None

    async def check_by_email(self, email: str) -> bool:
        collection = MongoHelper.get_collection("accounts")
        return collection.find_one({"email": email}, {"_id": 1}) is not None

    async def update_access_token(self, account_id: str, token: str) -> None:
        collection = MongoHelper.get_collection("accounts")
        collection.update_one({"_id": ObjectId(account_id)}, {"$set": {"accessToken": token}})

    async def load_by_token(self, token: str, role: str | None = None) -> AccountModel | None:
        collection = MongoHelper.get_collection("accounts")
        account = collection.find_one(
            {
                "accessToken": token,
                "$or": [{"role": role}, {"role": "admin"}],
            },
            {"_id": 1, "name": 1, "email": 1, "password": 1, "accessToken": 1, "role": 1},
        )
        return self._to_model(account) if account else None

    @staticmethod
    def _to_model(account: dict) -> AccountModel:
        model = AccountModel(
            id=str(account["_id"]),
            name=account.get("name", ""),
            email=account.get("email", ""),
            password=account.get("password", ""),
        )
        model.access_token = account.get("accessToken") or account.get("access_token")
        model.role = account.get("role")
        return model
