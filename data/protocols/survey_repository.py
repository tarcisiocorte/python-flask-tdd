from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from domain.models.survey import SurveyModel
from domain.usecases.add_survey import AddSurveyParams


class AddSurveyRepository(ABC):
    @abstractmethod
    async def add(self, data: AddSurveyParams) -> None:
        pass


class LoadSurveysRepository(ABC):
    @abstractmethod
    async def load_all(self, account_id: str) -> List[SurveyModel]:
        pass


class LoadSurveyByIdRepository(ABC):
    @abstractmethod
    async def load_by_id(self, survey_id: str) -> SurveyModel | None:
        pass


class CheckSurveyByIdRepository(ABC):
    @abstractmethod
    async def check_by_id(self, survey_id: str) -> bool:
        pass


class LoadAnswersBySurveyRepository(ABC):
    @abstractmethod
    async def load_answers(self, survey_id: str) -> List[str]:
        pass
