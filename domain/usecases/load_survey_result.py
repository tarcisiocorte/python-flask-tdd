from abc import ABC, abstractmethod

from domain.models.survey_result import SurveyResultModel


class LoadSurveyResult(ABC):
    @abstractmethod
    async def load(self, survey_id: str, account_id: str) -> SurveyResultModel:
        pass
