from __future__ import annotations

from domain.usecases.add_account import AddAccount, AddAccountModel
from domain.models.account import AccountModel
from data.protocols.encrypter import Encrypter, Hasher
from data.protocols.add_account_repository import (
    AddAccountRepository,
    CheckAccountByEmailRepository,
)


class DbAddAccount(AddAccount):
    def __init__(
        self,
        hasher: Hasher | Encrypter,
        add_account_repository: AddAccountRepository,
        check_account_by_email_repository: CheckAccountByEmailRepository | None = None,
    ):
        self.hasher = hasher
        self.add_account_repository = add_account_repository
        self.check_account_by_email_repository = check_account_by_email_repository

    async def add(self, account: AddAccountModel) -> AccountModel | bool | None:
        if self.check_account_by_email_repository:
            exists = await self.check_account_by_email_repository.check_by_email(account.email)
            if exists:
                return None
        hash_method = getattr(self.hasher, "hash", self.hasher.encrypt)
        hashed_password = await hash_method(account.password)
        account_with_hashed_password = AddAccountModel(
            name=account.name,
            email=account.email,
            password=hashed_password
        )
        return await self.add_account_repository.add(account_with_hashed_password)
