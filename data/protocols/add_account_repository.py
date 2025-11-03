from abc import ABC, abstractmethod
from domain.usecases.add_account import AddAccountModel
from domain.models.account import AccountModel


class AddAccountRepository(ABC):
    @abstractmethod
    async def add(self, account: AddAccountModel) -> AccountModel:
        pass
