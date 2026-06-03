from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class AuthenticationParams:
    email: str
    password: str


@dataclass
class AuthenticationModel:
    access_token: str
    name: str


class Authentication(ABC):
    @abstractmethod
    async def auth(self, params: AuthenticationParams) -> Optional[AuthenticationModel]:
        pass
