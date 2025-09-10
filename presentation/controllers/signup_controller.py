from protocols.signup_protocols import HttpResponse, HttpRequest, Controller, EmailValidator, AddAccount, AddAccountModel
from errors.missing_param_error import MissingParamError
from errors.invalid_param_error import InvalidParamError
from presentation.helpers.http_helper import bad_request, server_error, ok


class SignUpController(Controller):
    def __init__(self, email_validator: EmailValidator, add_account: AddAccount):
        self.email_validator = email_validator
        self.add_account = add_account

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            required_fields = ['name', 'email', 'password', 'passwordConfirmation']
            for field in required_fields:
                if not http_request.body.get(field):
                    return bad_request(MissingParamError(field))

            name = http_request.body['name']
            email = http_request.body['email']
            password = http_request.body['password']
            password_confirmation = http_request.body['passwordConfirmation']

            if password != password_confirmation:
                return bad_request(InvalidParamError('passwordConfirmation'))

            is_valid = self.email_validator.is_valid(email)
            if not is_valid:
                return bad_request(InvalidParamError('email'))

            account = self.add_account.add(AddAccountModel(
                name=name,
                email=email,
                password=password
            ))

            return ok(account)

        except Exception:
            return server_error()
