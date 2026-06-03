from domain.usecases import CheckSurveyById, LoadSurveyResult
from presentation.controllers._helpers import request_data, run_async
from presentation.errors import InvalidParamError
from presentation.helpers.http_helper import forbidden, ok, server_error
from presentation.protocols import Controller, HttpRequest, HttpResponse


class LoadSurveyResultController(Controller):
    def __init__(
        self,
        check_survey_by_id: CheckSurveyById,
        load_survey_result: LoadSurveyResult,
    ):
        self.check_survey_by_id = check_survey_by_id
        self.load_survey_result = load_survey_result

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            data = request_data(http_request)
            survey_id = data["survey_id"] if "survey_id" in data else data["surveyId"]
            account_id = data.get("account_id") or data.get("accountId")
            exists = run_async(self.check_survey_by_id.check_by_id(survey_id))
            if not exists:
                return forbidden(InvalidParamError("surveyId"))
            survey_result = run_async(self.load_survey_result.load(survey_id, account_id))
            return ok(survey_result)
        except Exception as error:
            return server_error(error)
