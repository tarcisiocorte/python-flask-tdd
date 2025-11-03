from abc import ABC, abstractmethod


class EmailValidator(ABC):
    @abstractmethod
    def is_valid(self, email: str) -> bool:
        pass

