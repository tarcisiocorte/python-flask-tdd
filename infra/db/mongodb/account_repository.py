"""MongoDB Account Repository implementation."""
from typing import Dict
from data.protocols.add_account_repository import AddAccountRepository
from domain.usecases.add_account import AddAccountModel
from domain.models.account import AccountModel
from infra.db.mongodb.helpers.mongo_helper import MongoHelper


class AccountMongoRepository(AddAccountRepository):
    """MongoDB implementation of AddAccountRepository."""

    async def add(self, account_data: AddAccountModel) -> AccountModel:
        """
        Add a new account to MongoDB.

        Args:
            account_data: Account data to be added.

        Returns:
            The created account with id.
        """
        collection = MongoHelper.get_collection("accounts")
        
        # Convert dataclass to dict for MongoDB insertion
        account_dict = {
            "name": account_data.name,
            "email": account_data.email,
            "password": account_data.password
        }
        
        # Insert into MongoDB
        result = collection.insert_one(account_dict)
        
        # Return AccountModel with the generated id
        return AccountModel(
            id=str(result.inserted_id),
            name=account_data.name,
            email=account_data.email,
            password=account_data.password
        )

