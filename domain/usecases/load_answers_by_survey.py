from abc import ABC, abstractmethod
from typing import List


class LoadAnswersBySurvey(ABC):
    @abstractmethod
    async def load_answers(self, survey_id: str) -> List[str]:
        pass
