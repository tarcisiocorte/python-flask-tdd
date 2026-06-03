from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Validation(ABC):
    @abstractmethod
    def validate(self, input_data: Any) -> Exception | None:
        pass
