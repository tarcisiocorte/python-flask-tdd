from domain.usecases import LoadSurveys
from presentation.controllers._helpers import request_data, run_async
from presentation.helpers.http_helper import no_content, ok, server_error
from presentation.protocols import Controller, HttpRequest, HttpResponse


class LoadSurveysController(Controller):
    def __init__(self, load_surveys: LoadSurveys):
        self.load_surveys = load_surveys

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            data = request_data(http_request)
            surveys = run_async(self.load_surveys.load(data.get("account_id") or data.get("accountId")))
            return ok(surveys) if surveys else no_content()
        except Exception as error:
            return server_error(error)
