from __future__ import annotations

from domain.usecases.save_survey_result import SaveSurveyResult, SaveSurveyResultModel
from domain.models.survey_result import SurveyResultModel
from data.protocols.save_survey_result_repository import (
    LoadSurveyResultRepository,
    SaveSurveyResultRepository,
)


class DbSaveSurveyResult(SaveSurveyResult):
    def __init__(
        self,
        save_survey_result_repository: SaveSurveyResultRepository,
        load_survey_result_repository: LoadSurveyResultRepository | None = None,
    ):
        self.save_survey_result_repository = save_survey_result_repository
        self.load_survey_result_repository = load_survey_result_repository or save_survey_result_repository

    async def save(self, data: SaveSurveyResultModel) -> SurveyResultModel:
        saved = await self.save_survey_result_repository.save(data)
        if hasattr(self.load_survey_result_repository, "load_by_survey_id"):
            loaded = await self.load_survey_result_repository.load_by_survey_id(
                data.survey_id, data.account_id
            )
            if loaded:
                return loaded
        return saved
