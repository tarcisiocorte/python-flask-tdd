from typing import List

from domain.models.survey import SurveyModel
from domain.usecases import (
    AddSurvey,
    AddSurveyParams,
    CheckSurveyById,
    LoadAnswersBySurvey,
    LoadSurveys,
)
from data.protocols import (
    AddSurveyRepository,
    CheckSurveyByIdRepository,
    LoadAnswersBySurveyRepository,
    LoadSurveysRepository,
)


class DbAddSurvey(AddSurvey):
    def __init__(self, add_survey_repository: AddSurveyRepository):
        self.add_survey_repository = add_survey_repository

    async def add(self, params: AddSurveyParams) -> None:
        await self.add_survey_repository.add(params)


class DbLoadSurveys(LoadSurveys):
    def __init__(self, load_surveys_repository: LoadSurveysRepository):
        self.load_surveys_repository = load_surveys_repository

    async def load(self, account_id: str) -> List[SurveyModel]:
        return await self.load_surveys_repository.load_all(account_id)


class DbCheckSurveyById(CheckSurveyById):
    def __init__(self, check_survey_by_id_repository: CheckSurveyByIdRepository):
        self.check_survey_by_id_repository = check_survey_by_id_repository

    async def check_by_id(self, survey_id: str) -> bool:
        return await self.check_survey_by_id_repository.check_by_id(survey_id)


class DbLoadAnswersBySurvey(LoadAnswersBySurvey):
    def __init__(self, load_answers_by_survey_repository: LoadAnswersBySurveyRepository):
        self.load_answers_by_survey_repository = load_answers_by_survey_repository

    async def load_answers(self, survey_id: str) -> List[str]:
        return await self.load_answers_by_survey_repository.load_answers(survey_id)
