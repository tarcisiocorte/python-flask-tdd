from abc import ABC, abstractmethod


class Encrypter(ABC):
    @abstractmethod
    async def encrypt(self, value: str) -> str:
        pass
    
    @abstractmethod
    async def compare(self, value: str, hash: str) -> bool:
        pass
