from __future__ import annotations

from abc import ABC, abstractmethod
from domain.usecases.add_account import AddAccountModel
from domain.models.account import AccountModel


class AddAccountRepository(ABC):
    @abstractmethod
    async def add(self, account: AddAccountModel) -> bool | AccountModel:
        pass


class CheckAccountByEmailRepository(ABC):
    @abstractmethod
    async def check_by_email(self, email: str) -> bool:
        pass


class LoadAccountByEmailRepository(ABC):
    @abstractmethod
    async def load_by_email(self, email: str) -> AccountModel | None:
        pass


class LoadAccountByTokenRepository(ABC):
    @abstractmethod
    async def load_by_token(self, token: str, role: str | None = None) -> AccountModel | None:
        pass


class UpdateAccessTokenRepository(ABC):
    @abstractmethod
    async def update_access_token(self, account_id: str, token: str) -> None:
        pass
