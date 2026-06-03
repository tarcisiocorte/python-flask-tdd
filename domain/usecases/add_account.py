from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from domain.models.account import AccountModel


@dataclass
class AddAccountModel:
    name: str
    email: str
    password: str


class AddAccount(ABC):
    @abstractmethod
    async def add(self, account: AddAccountModel) -> Optional[AccountModel]:
        pass 
