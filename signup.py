from signup_protocols import HttpRequest, HttpResponse, AddAccount, AddAccountModel
from errors.missing_param_error import MissingParamError
from errors.server_error import ServerError


class SignUpController:
    def __init__(self, add_account: AddAccount):
        self.add_account = add_account

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:

            required_fields = ["name", "email", "password", "passwordConfirmation"]
            for field in required_fields:
                if not http_request.body.get(field):
                    raise MissingParamError(field)

            if http_request.body["password"] != http_request.body["passwordConfirmation"]:
                return HttpResponse(
                    status_code=400,
                    body={"error": "Password confirmation does not match password"}
                )

            account = self.add_account.add(AddAccountModel(
                name=http_request.body["name"],
                email=http_request.body["email"],
                password=http_request.body["password"]
            ))

            return HttpResponse(
                status_code=200,
                body={
                    "id": account.id,
                    "name": account.name,
                    "email": account.email,
                    "password": account.password
                }
            )
        except MissingParamError as e:
            return HttpResponse(
                status_code=400,
                body={"error": str(e)}
            )
        except Exception:
            return HttpResponse(
                status_code=500,
                body={"error": "Internal server error"}
            )
