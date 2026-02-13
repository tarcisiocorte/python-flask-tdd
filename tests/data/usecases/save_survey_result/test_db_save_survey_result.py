import unittest
import asyncio
from unittest.mock import AsyncMock, patch
from datetime import datetime
from typing import NamedTuple

from data.usecases.save_survey_result.db_save_survey_result import DbSaveSurveyResult
from domain.usecases.save_survey_result import SaveSurveyResultModel
from domain.models.survey_result import SurveyResultModel
from data.protocols.save_survey_result_repository import SaveSurveyResultRepository


class SaveSurveyResultRepositoryStub(SaveSurveyResultRepository):
    """Stub implementation for testing"""
    
    async def save(self, data: SaveSurveyResultModel) -> SurveyResultModel:
        return SurveyResultModel(
            id="any_id",
            survey_id=data.survey_id,
            account_id=data.account_id,
            answer=data.answer,
            date=data.date
        )


class SutTypes(NamedTuple):
    sut: DbSaveSurveyResult
    save_survey_result_repository_stub: SaveSurveyResultRepositoryStub


def make_sut() -> SutTypes:
    """Factory function to create system under test with dependencies"""
    save_survey_result_repository_stub = SaveSurveyResultRepositoryStub()
    sut = DbSaveSurveyResult(save_survey_result_repository_stub)
    return SutTypes(
        sut=sut,
        save_survey_result_repository_stub=save_survey_result_repository_stub
    )


def make_fake_survey_result_data() -> SaveSurveyResultModel:
    """Factory function to create fake survey result data"""
    return SaveSurveyResultModel(
        survey_id="any_survey_id",
        account_id="any_account_id",
        answer="any_answer",
        date=datetime(2020, 1, 1, 0, 0, 0)
    )


class TestDbSaveSurveyResult(unittest.TestCase):
    """Test suite for DbSaveSurveyResult use case"""
    
    def test_should_call_save_survey_result_repository_with_correct_values(self):
        """
        First test: Should call SaveSurveyResultRepository with correct values
        This verifies that DbSaveSurveyResult delegates to the repository correctly
        """
        sut_types = make_sut()
        sut = sut_types.sut
        save_survey_result_repository_stub = sut_types.save_survey_result_repository_stub
        
        # Create a spy to monitor the repository method call
        with patch.object(
            save_survey_result_repository_stub,
            'save',
            new_callable=AsyncMock
        ) as save_spy:
            survey_result_data = make_fake_survey_result_data()
            
            # Act: call the save method
            asyncio.run(sut.save(survey_result_data))
            
            # Assert: verify the repository was called with correct data
            save_spy.assert_called_once_with(survey_result_data)


if __name__ == '__main__':
    unittest.main()

