from __future__ import annotations

from presentation.protocols import HttpRequest, HttpResponse, Controller
from presentation.protocols.email_validator import EmailValidator
from domain.usecases import AddAccount, AddAccountModel, Authentication, AuthenticationParams
from presentation.controllers._helpers import request_data, run_async
from presentation.errors import EmailInUseError, InvalidParamError, MissingParamError
from presentation.helpers.http_helper import bad_request, forbidden, ok, server_error
from presentation.protocols import Validation
from validation.validators import (
    CompareFieldsValidation,
    EmailValidation,
    PasswordStrengthValidation,
    RequiredFieldValidation,
    ValidationComposite,
)


class SignUpController(Controller):
    def __init__(
        self,
        add_account_or_email_validator: AddAccount | EmailValidator,
        validation_or_add_account: Validation | AddAccount,
        authentication: Authentication | None = None,
    ):
        if authentication is None:
            email_validator = add_account_or_email_validator
            self.add_account = validation_or_add_account
            self.validation = ValidationComposite([
                RequiredFieldValidation("name"),
                RequiredFieldValidation("email"),
                RequiredFieldValidation("password"),
                RequiredFieldValidation("passwordConfirmation"),
                CompareFieldsValidation("password", "passwordConfirmation"),
                PasswordStrengthValidation("password"),
                EmailValidation("email", email_validator),
            ])
            self.authentication = None
        else:
            self.add_account = add_account_or_email_validator
            self.validation = validation_or_add_account
            self.authentication = authentication

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            data = request_data(http_request)
            error = self.validation.validate(data)
            if error:
                return bad_request(error)

            name = data["name"]
            email = data["email"]
            password = data["password"]

            account = run_async(self.add_account.add(AddAccountModel(
                name=name,
                email=email,
                password=password
            )))
            if not account:
                return forbidden(EmailInUseError())

            if self.authentication:
                authentication_model = run_async(self.authentication.auth(AuthenticationParams(
                    email=email,
                    password=password,
                )))
                return ok(authentication_model)
            return ok(account)
        except Exception as error:
            return server_error(error)
