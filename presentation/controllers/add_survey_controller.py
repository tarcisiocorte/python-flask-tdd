from dataclasses import replace
from datetime import datetime

from domain.usecases import AddSurvey, AddSurveyParams
from presentation.controllers._helpers import request_data, run_async
from presentation.helpers.http_helper import bad_request, no_content, server_error
from presentation.protocols import Controller, HttpRequest, HttpResponse, Validation


class AddSurveyController(Controller):
    def __init__(self, validation: Validation, add_survey: AddSurvey):
        self.validation = validation
        self.add_survey = add_survey

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            data = request_data(http_request)
            error = self.validation.validate(data)
            if error:
                return bad_request(error)
            params = AddSurveyParams(
                question=data["question"],
                answers=data["answers"],
                date=datetime.utcnow(),
            )
            run_async(self.add_survey.add(params))
            return no_content()
        except Exception as error:
            return server_error(error)
