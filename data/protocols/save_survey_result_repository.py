from __future__ import annotations

from abc import ABC, abstractmethod
from domain.usecases.save_survey_result import SaveSurveyResultModel
from domain.models.survey_result import SurveyResultModel


class SaveSurveyResultRepository(ABC):
    @abstractmethod
    async def save(self, data: SaveSurveyResultModel) -> None:
        pass


class LoadSurveyResultRepository(ABC):
    @abstractmethod
    async def load_by_survey_id(
        self, survey_id: str, account_id: str
    ) -> SurveyResultModel | None:
        pass
