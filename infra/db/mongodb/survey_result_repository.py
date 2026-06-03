from __future__ import annotations

from collections import Counter
from datetime import datetime

from bson import ObjectId

from data.protocols import LoadSurveyResultRepository, SaveSurveyResultRepository
from domain.models.survey_result import SurveyResultAnswerModel, SurveyResultModel
from domain.usecases.save_survey_result import SaveSurveyResultParams
from infra.db.mongodb.helpers.mongo_helper import MongoHelper


class SurveyResultMongoRepository(SaveSurveyResultRepository, LoadSurveyResultRepository):
    async def save(self, data: SaveSurveyResultParams) -> None:
        collection = MongoHelper.get_collection("surveyResults")
        collection.find_one_and_update(
            {
                "surveyId": ObjectId(data.survey_id),
                "accountId": ObjectId(data.account_id),
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
        survey = MongoHelper.get_collection("surveys").find_one({"_id": ObjectId(survey_id)})
        if not survey:
            return None
        rows = list(MongoHelper.get_collection("surveyResults").find({
            "surveyId": ObjectId(survey_id)
        }))
        if not rows:
            return None
        total = len(rows)
        counts = Counter(row["answer"] for row in rows)
        current = next(
            (
                row["answer"]
                for row in rows
                if row.get("accountId") == ObjectId(account_id)
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
