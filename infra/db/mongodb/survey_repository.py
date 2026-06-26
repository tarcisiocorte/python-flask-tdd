from __future__ import annotations

from bson import ObjectId

from data.protocols import (
    AddSurveyRepository,
    CheckSurveyByIdRepository,
    LoadAnswersBySurveyRepository,
    LoadSurveyByIdRepository,
    LoadSurveysRepository,
)
from domain.models.survey import SurveyAnswerModel, SurveyModel
from domain.usecases.add_survey import AddSurveyParams
from infra.db.mongodb.helpers.mongo_helper import MongoHelper


def _to_object_id(value: str) -> ObjectId | None:
    return ObjectId(value) if ObjectId.is_valid(value) else None


class SurveyMongoRepository(
    AddSurveyRepository,
    CheckSurveyByIdRepository,
    LoadAnswersBySurveyRepository,
    LoadSurveyByIdRepository,
    LoadSurveysRepository,
):
    async def add(self, data: AddSurveyParams) -> None:
        collection = MongoHelper.get_collection("surveys")
        collection.insert_one({
            "question": data.question,
            "answers": [
                answer if isinstance(answer, dict) else answer.__dict__
                for answer in data.answers
            ],
            "date": data.date,
        })

    async def load_all(self, account_id: str) -> list[SurveyModel]:
        surveys = list(MongoHelper.get_collection("surveys").find())
        results = MongoHelper.get_collection("surveyResults")
        account_object_id = _to_object_id(account_id)
        return [
            self._to_model(
                survey,
                did_answer=(
                    account_object_id is not None
                    and results.find_one({
                        "surveyId": survey["_id"],
                        "accountId": account_object_id,
                    }) is not None
                ),
            )
            for survey in surveys
        ]

    async def load_by_id(self, survey_id: str) -> SurveyModel | None:
        object_id = _to_object_id(survey_id)
        if object_id is None:
            return None
        survey = MongoHelper.get_collection("surveys").find_one({"_id": object_id})
        return self._to_model(survey) if survey else None

    async def check_by_id(self, survey_id: str) -> bool:
        object_id = _to_object_id(survey_id)
        if object_id is None:
            return False
        return MongoHelper.get_collection("surveys").find_one(
            {"_id": object_id}, {"_id": 1}
        ) is not None

    async def load_answers(self, survey_id: str) -> list[str]:
        object_id = _to_object_id(survey_id)
        if object_id is None:
            return []
        survey = MongoHelper.get_collection("surveys").find_one(
            {"_id": object_id}, {"answers": 1}
        )
        return [answer["answer"] for answer in survey.get("answers", [])] if survey else []

    @staticmethod
    def _to_model(survey: dict, did_answer: bool = False) -> SurveyModel:
        return SurveyModel(
            id=str(survey["_id"]),
            question=survey["question"],
            answers=[
                SurveyAnswerModel(
                    answer=answer["answer"],
                    image=answer.get("image"),
                )
                for answer in survey.get("answers", [])
            ],
            date=survey.get("date"),
            did_answer=did_answer,
        )
