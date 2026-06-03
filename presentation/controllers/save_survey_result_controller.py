from dataclasses import replace
from datetime import datetime

from domain.usecases import LoadAnswersBySurvey, SaveSurveyResult, SaveSurveyResultParams
from presentation.controllers._helpers import request_data, run_async
from presentation.errors import InvalidParamError
from presentation.helpers.http_helper import forbidden, ok, server_error
from presentation.protocols import Controller, HttpRequest, HttpResponse


class SaveSurveyResultController(Controller):
    def __init__(
        self,
        load_answers_by_survey: LoadAnswersBySurvey,
        save_survey_result: SaveSurveyResult,
    ):
        self.load_answers_by_survey = load_answers_by_survey
        self.save_survey_result = save_survey_result

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            data = request_data(http_request)
            survey_id = data["survey_id"] if "survey_id" in data else data["surveyId"]
            answer = data["answer"]
            answers = run_async(self.load_answers_by_survey.load_answers(survey_id))
            if not answers:
                return forbidden(InvalidParamError("surveyId"))
            if answer not in answers:
                return forbidden(InvalidParamError("answer"))
            result = run_async(self.save_survey_result.save(SaveSurveyResultParams(
                survey_id=survey_id,
                account_id=data.get("account_id") or data.get("accountId"),
                answer=answer,
            )))
            return ok(result)
        except Exception as error:
            return server_error(error)
