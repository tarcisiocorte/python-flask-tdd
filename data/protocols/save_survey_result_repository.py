from abc import ABC, abstractmethod
from domain.usecases.save_survey_result import SaveSurveyResultModel
from domain.models.survey_result import SurveyResultModel


class SaveSurveyResultRepository(ABC):
    """Repository protocol for saving survey results"""
    
    @abstractmethod
    async def save(self, data: SaveSurveyResultModel) -> SurveyResultModel:
        """
        Saves a survey result to the database
        
        Args:
            data: Survey result data to save
            
        Returns:
            The saved survey result with generated ID
        """
        pass

