import asyncio
from unittest.mock import patch

from domain.usecases.save_survey_result import SaveSurveyResultParams
from infra.db.mongodb.survey_result_repository import SurveyResultMongoRepository


def test_save_ignores_invalid_object_ids_without_querying_db():
    sut = SurveyResultMongoRepository()
    params = SaveSurveyResultParams(
        survey_id="not-an-object-id",
        account_id="also-not-an-object-id",
        answer="answer",
    )

    with patch("infra.db.mongodb.survey_result_repository.MongoHelper") as mongo_helper:
        result = asyncio.run(sut.save(params))

    assert result is None
    mongo_helper.get_collection.assert_not_called()


def test_load_by_survey_id_returns_none_for_invalid_survey_id_without_querying_db():
    sut = SurveyResultMongoRepository()

    with patch("infra.db.mongodb.survey_result_repository.MongoHelper") as mongo_helper:
        result = asyncio.run(sut.load_by_survey_id("not-an-object-id", "account_id"))

    assert result is None
    mongo_helper.get_collection.assert_not_called()
