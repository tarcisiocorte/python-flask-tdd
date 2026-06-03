from __future__ import annotations

import uuid
from data.protocols.add_account_repository import (
    AddAccountRepository,
    CheckAccountByEmailRepository,
    LoadAccountByEmailRepository,
    LoadAccountByTokenRepository,
    UpdateAccessTokenRepository,
)
from domain.usecases.add_account import AddAccountModel
from domain.models.account import AccountModel


class InMemoryAddAccountRepository(
    AddAccountRepository,
    CheckAccountByEmailRepository,
    LoadAccountByEmailRepository,
    LoadAccountByTokenRepository,
    UpdateAccessTokenRepository,
):
    def __init__(self):
        # In a real application, this would be a database
        self.accounts = []
    
    async def add(self, account: AddAccountModel) -> AccountModel:
        # Generate a unique ID for the account
        account_id = str(uuid.uuid4())
        
        # Create the account model
        new_account = AccountModel(
            id=account_id,
            name=account.name,
            email=account.email,
            password=account.password  # In production, this should be hashed
        )
        
        # Store the account (in memory for this example)
        self.accounts.append(new_account)
        return new_account

    async def check_by_email(self, email: str) -> bool:
        return any(account.email == email for account in self.accounts)

    async def load_by_email(self, email: str) -> AccountModel | None:
        return next((account for account in self.accounts if account.email == email), None)

    async def update_access_token(self, account_id: str, token: str) -> None:
        account = next((item for item in self.accounts if item.id == account_id), None)
        if account:
            account.access_token = token

    async def load_by_token(self, token: str, role: str | None = None) -> AccountModel | None:
        for account in self.accounts:
            if account.access_token == token and (account.role == role or account.role == "admin"):
                return account
        return None
