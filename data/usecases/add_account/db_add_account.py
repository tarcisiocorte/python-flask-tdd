from domain.usecases.add_account import AddAccount, AddAccountModel
from domain.models.account import AccountModel
from data.protocols.encrypter import Encrypter
from data.protocols.add_account_repository import AddAccountRepository


class DbAddAccount(AddAccount):
    def __init__(self, encrypter: Encrypter, add_account_repository: AddAccountRepository):
        self.encrypter = encrypter
        self.add_account_repository = add_account_repository

    async def add(self, account: AddAccountModel) -> AccountModel:
        hashed_password = await self.encrypter.encrypt(account.password)
        account_with_hashed_password = AddAccountModel(
            name=account.name,
            email=account.email,
            password=hashed_password
        )
        return await self.add_account_repository.add(account_with_hashed_password)

