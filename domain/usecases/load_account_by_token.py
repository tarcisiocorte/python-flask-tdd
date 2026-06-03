from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from domain.models.account import AccountModel


class LoadAccountByToken(ABC):
    @abstractmethod
    async def load(self, access_token: str, role: str | None = None) -> Optional[AccountModel]:
        pass
