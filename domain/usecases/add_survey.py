from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class AddSurveyAnswerParams:
    answer: str
    image: Optional[str] = None


@dataclass
class AddSurveyParams:
    question: str
    answers: List[AddSurveyAnswerParams]
    date: datetime | None = None


class AddSurvey(ABC):
    @abstractmethod
    async def add(self, params: AddSurveyParams) -> None:
        pass
