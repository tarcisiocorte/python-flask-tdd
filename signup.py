from protocols.http import HttpRequest, HttpResponse
from errors.missing_param_error import MissingParamError


class SignUpController:
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            if not http_request.body.get("name"):
                raise MissingParamError("name")
            
            if not http_request.body.get("email"):
                raise MissingParamError("email")
            
            if not http_request.body.get("password"):
                raise MissingParamError("password")
            
            if not http_request.body.get("passwordConfirmation"):
                raise MissingParamError("passwordConfirmation")

            if http_request.body["password"] != http_request.body["passwordConfirmation"]:
                return HttpResponse(
                    status_code=400,
                    body={"error": "Password confirmation does not match password"}
                )

            return HttpResponse(
                status_code=200,
                body={"message": "User signed up successfully"}
            )
        except MissingParamError as e:
            return HttpResponse(
                status_code=400,
                body={"error": str(e)}
            )
