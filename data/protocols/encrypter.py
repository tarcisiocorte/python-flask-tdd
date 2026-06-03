from __future__ import annotations

from abc import ABC, abstractmethod


class Encrypter(ABC):
    @abstractmethod
    async def encrypt(self, value: str) -> str:
        pass


class Decrypter(ABC):
    @abstractmethod
    async def decrypt(self, value: str) -> str | None:
        pass


class Hasher(ABC):
    @abstractmethod
    async def hash(self, value: str) -> str:
        pass


class HashComparer(ABC):
    @abstractmethod
    async def compare(self, value: str, digest: str) -> bool:
        pass
