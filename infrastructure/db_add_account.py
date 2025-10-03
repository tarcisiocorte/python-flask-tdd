from domain.usecases.add_account import AddAccount, AddAccountModel
from domain.models.account import AccountModel
from protocols.encrypter import Encrypter


class DbAddAccount(AddAccount):
    def __init__(self, encrypter: Encrypter):
        self.encrypter = encrypter

    async def add(self, account: AddAccountModel) -> AccountModel:
        await self.encrypter.encrypt(account.password)
        return None
