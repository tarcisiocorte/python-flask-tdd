from domain.usecases.save_survey_result import SaveSurveyResult, SaveSurveyResultModel
from domain.models.survey_result import SurveyResultModel
from data.protocols.save_survey_result_repository import SaveSurveyResultRepository


class DbSaveSurveyResult(SaveSurveyResult):
    """Database implementation of SaveSurveyResult use case"""
    
    def __init__(self, save_survey_result_repository: SaveSurveyResultRepository):
        self.save_survey_result_repository = save_survey_result_repository
    
    async def save(self, data: SaveSurveyResultModel) -> SurveyResultModel:
        """
        Saves a survey result using the repository
        
        Args:
            data: Survey result data to save
            
        Returns:
            The saved survey result
        """
        survey_result = await self.save_survey_result_repository.save(data)
        return survey_result

