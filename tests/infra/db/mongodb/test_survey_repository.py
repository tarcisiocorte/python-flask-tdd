import asyncio
from unittest.mock import Mock, patch

from infra.db.mongodb.survey_repository import SurveyMongoRepository


def test_check_by_id_returns_false_for_invalid_object_id_without_querying_db():
    sut = SurveyMongoRepository()

    with patch("infra.db.mongodb.survey_repository.MongoHelper") as mongo_helper:
        result = asyncio.run(sut.check_by_id("not-an-object-id"))

    assert result is False
    mongo_helper.get_collection.assert_not_called()


def test_load_by_id_returns_none_for_invalid_object_id_without_querying_db():
    sut = SurveyMongoRepository()

    with patch("infra.db.mongodb.survey_repository.MongoHelper") as mongo_helper:
        result = asyncio.run(sut.load_by_id("not-an-object-id"))

    assert result is None
    mongo_helper.get_collection.assert_not_called()


def test_load_answers_returns_empty_list_for_invalid_object_id_without_querying_db():
    sut = SurveyMongoRepository()

    with patch("infra.db.mongodb.survey_repository.MongoHelper") as mongo_helper:
        result = asyncio.run(sut.load_answers("not-an-object-id"))

    assert result == []
    mongo_helper.get_collection.assert_not_called()


def test_load_all_does_not_query_results_for_invalid_account_id():
    sut = SurveyMongoRepository()
    surveys_collection = Mock()
    surveys_collection.find.return_value = [
        {"_id": "survey_id", "question": "Question?", "answers": []}
    ]
    results_collection = Mock()

    with patch("infra.db.mongodb.survey_repository.MongoHelper") as mongo_helper:
        mongo_helper.get_collection.side_effect = [
            surveys_collection,
            results_collection,
        ]
        result = asyncio.run(sut.load_all("not-an-object-id"))

    assert result[0].did_answer is False
    results_collection.find_one.assert_not_called()
