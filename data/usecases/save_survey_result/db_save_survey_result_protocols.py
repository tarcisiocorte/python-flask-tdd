# Re-export all protocols needed for db_save_survey_result
from domain.usecases.save_survey_result import SaveSurveyResult, SaveSurveyResultModel
from domain.models.survey_result import SurveyResultModel
from data.protocols.save_survey_result_repository import SaveSurveyResultRepository

__all__ = [
    "SaveSurveyResult",
    "SaveSurveyResultModel",
    "SurveyResultModel",
    "SaveSurveyResultRepository",
]

