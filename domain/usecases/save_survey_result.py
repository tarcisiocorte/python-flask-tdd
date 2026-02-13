from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from domain.models.survey_result import SurveyResultModel


@dataclass
class SaveSurveyResultModel:
    """Data required to save a survey result"""
    survey_id: str
    account_id: str
    answer: str
    date: datetime


class SaveSurveyResult(ABC):
    """Save Survey Result use case interface"""
    
    @abstractmethod
    async def save(self, data: SaveSurveyResultModel) -> SurveyResultModel:
        """
        Saves a survey result
        
        Args:
            data: Survey result data to save
            
        Returns:
            The saved survey result
        """
        pass

