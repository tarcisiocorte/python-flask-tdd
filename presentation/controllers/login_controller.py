from domain.usecases import Authentication
from presentation.controllers._helpers import request_data, run_async
from presentation.helpers.http_helper import bad_request, ok, server_error, unauthorized
from presentation.protocols import Controller, HttpRequest, HttpResponse, Validation


class LoginController(Controller):
    def __init__(self, authentication: Authentication, validation: Validation):
        self.authentication = authentication
        self.validation = validation

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            data = request_data(http_request)
            error = self.validation.validate(data)
            if error:
                return bad_request(error)
            authentication_model = run_async(self.authentication.auth(data))
            if not authentication_model:
                return unauthorized()
            return ok(authentication_model)
        except Exception as error:
            return server_error(error)
