from __future__ import annotations

from collections import Counter
from datetime import datetime

from bson import ObjectId

from data.protocols import LoadSurveyResultRepository, SaveSurveyResultRepository
from domain.models.survey_result import SurveyResultAnswerModel, SurveyResultModel
from domain.usecases.save_survey_result import SaveSurveyResultParams
from infra.db.mongodb.helpers.mongo_helper import MongoHelper


def _to_object_id(value: str) -> ObjectId | None:
    return ObjectId(value) if ObjectId.is_valid(value) else None


class SurveyResultMongoRepository(SaveSurveyResultRepository, LoadSurveyResultRepository):
    async def save(self, data: SaveSurveyResultParams) -> None:
        survey_object_id = _to_object_id(data.survey_id)
        account_object_id = _to_object_id(data.account_id)
        if survey_object_id is None or account_object_id is None:
            return None

        collection = MongoHelper.get_collection("surveyResults")
        collection.find_one_and_update(
            {
                "surveyId": survey_object_id,
                "accountId": account_object_id,
            },
            {
                "$set": {
                    "answer": data.answer,
                    "date": data.date or datetime.utcnow(),
                }
            },
            upsert=True,
        )

    async def load_by_survey_id(
        self, survey_id: str, account_id: str
    ) -> SurveyResultModel | None:
        survey_object_id = _to_object_id(survey_id)
        account_object_id = _to_object_id(account_id)
        if survey_object_id is None:
            return None

        survey = MongoHelper.get_collection("surveys").find_one({"_id": survey_object_id})
        if not survey:
            return None
        rows = list(MongoHelper.get_collection("surveyResults").find({
            "surveyId": survey_object_id
        }))
        if not rows:
            return None
        total = len(rows)
        counts = Counter(row["answer"] for row in rows)
        current = next(
            (
                row["answer"]
                for row in rows
                if account_object_id is not None and row.get("accountId") == account_object_id
            ),
            None,
        )
        answers = []
        for answer in survey.get("answers", []):
            count = counts.get(answer["answer"], 0)
            answers.append(SurveyResultAnswerModel(
                answer=answer["answer"],
                image=answer.get("image"),
                count=count,
                percent=round(count / total * 100) if total else 0,
                is_current_account_answer=answer["answer"] == current,
            ))
        answers.sort(key=lambda item: item.count, reverse=True)
        return SurveyResultModel(
            survey_id=str(survey["_id"]),
            question=survey["question"],
            date=survey.get("date"),
            answers=answers,
        )
