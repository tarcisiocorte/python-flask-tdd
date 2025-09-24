from abc import ABC, abstractmethod


class Encrypter(ABC):
    @abstractmethod
    async def encrypt(self, value: str) -> str:
        pass
