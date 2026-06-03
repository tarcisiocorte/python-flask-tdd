from domain.models.survey_result import SurveyResultAnswerModel, SurveyResultModel
from domain.usecases import LoadSurveyResult
from data.protocols import LoadSurveyByIdRepository, LoadSurveyResultRepository


class DbLoadSurveyResult(LoadSurveyResult):
    def __init__(
        self,
        load_survey_result_repository: LoadSurveyResultRepository,
        load_survey_by_id_repository: LoadSurveyByIdRepository,
    ):
        self.load_survey_result_repository = load_survey_result_repository
        self.load_survey_by_id_repository = load_survey_by_id_repository

    async def load(self, survey_id: str, account_id: str) -> SurveyResultModel:
        survey_result = await self.load_survey_result_repository.load_by_survey_id(
            survey_id, account_id
        )
        if survey_result:
            return survey_result
        survey = await self.load_survey_by_id_repository.load_by_id(survey_id)
        return SurveyResultModel(
            survey_id=survey.id,
            question=survey.question,
            date=survey.date,
            answers=[
                SurveyResultAnswerModel(
                    answer=answer.answer,
                    image=answer.image,
                    count=0,
                    percent=0,
                    is_current_account_answer=False,
                )
                for answer in survey.answers
            ],
        )
