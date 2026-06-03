from abc import ABC, abstractmethod


class CheckSurveyById(ABC):
    @abstractmethod
    async def check_by_id(self, survey_id: str) -> bool:
        pass
