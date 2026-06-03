from abc import ABC, abstractmethod
from typing import List

from domain.models.survey import SurveyModel


class LoadSurveys(ABC):
    @abstractmethod
    async def load(self, account_id: str) -> List[SurveyModel]:
        pass
