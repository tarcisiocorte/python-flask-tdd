from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from domain.models.survey_result import SurveyResultModel


@dataclass
class SaveSurveyResultParams:
    survey_id: str
    account_id: str
    answer: str
    date: datetime | None = None


SaveSurveyResultModel = SaveSurveyResultParams


class SaveSurveyResult(ABC):
    @abstractmethod
    async def save(self, data: SaveSurveyResultParams) -> SurveyResultModel:
        pass
