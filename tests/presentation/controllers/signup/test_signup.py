import unittest
import asyncio
from unittest.mock import Mock, AsyncMock
from presentation.controllers.signup.signup import SignUpController
from presentation.protocols.http import HttpRequest
from domain.usecases import AuthenticationModel
from domain.usecases.add_account import AddAccount, AddAccountModel
from domain.models.account import AccountModel
from presentation.protocols.email_validator import EmailValidator
from presentation.errors.server_error import ServerError
from presentation.errors import EmailInUseError, MissingParamError, InvalidParamError


def make_email_validator_stub(is_valid: bool = True) -> EmailValidator:
    class EmailValidatorStub(EmailValidator):
        def is_valid(self, email: str) -> bool:
            return is_valid
    return EmailValidatorStub()


def make_add_account_stub() -> AddAccount:
    class AddAccountStub(AddAccount):
        async def add(self, account: AddAccountModel) -> AccountModel:
            return AccountModel(
                id="valid_id",
                name="valid_name",
                email="valid_email@mail.com",
                password="Valid_password123"
            )
    return AddAccountStub()


def make_sut() -> SignUpController:
    email_validator_stub = make_email_validator_stub()
    add_account_stub = make_add_account_stub()
    return SignUpController(email_validator_stub, add_account_stub)


class TestSignUpController(unittest.TestCase):
    def test_should_return_400_if_no_name_provided(self):
        sut = make_sut()
        http_request = HttpRequest({
            "email": "any_email@mail.com",
            "password": "Valid_password123",
            "passwordConfirmation": "Valid_password123"
        })
        http_response = sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertIsInstance(http_response.body, MissingParamError)
        self.assertEqual(str(http_response.body), "Missing param: name")

    def test_should_return_400_if_no_email_provided(self):
        sut = make_sut()
        http_request = HttpRequest({
            "name": "any_name",
            "password": "Valid_password123",
            "passwordConfirmation": "Valid_password123"
        })
        http_response = sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertIsInstance(http_response.body, MissingParamError)
        self.assertEqual(str(http_response.body), "Missing param: email")

    def test_should_return_400_if_no_password_provided(self):
        sut = make_sut()
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "passwordConfirmation": "Valid_password123"
        })
        http_response = sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertIsInstance(http_response.body, MissingParamError)
        self.assertEqual(str(http_response.body), "Missing param: password")

    def test_should_return_400_if_no_password_confirmation_provided(self):
        sut = make_sut()
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "Valid_password123"
        })
        http_response = sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertIsInstance(http_response.body, MissingParamError)
        self.assertEqual(str(http_response.body), "Missing param: passwordConfirmation")

    def test_should_return_400_if_password_confirmation_fails(self):
        sut = make_sut()
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "Valid_password123",
            "passwordConfirmation": "invalid_confirmation"
        })
        http_response = sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertIsInstance(http_response.body, InvalidParamError)
        self.assertEqual(str(http_response.body), "Invalid param: passwordConfirmation")

    def test_should_return_400_if_email_is_invalid(self):
        email_validator_stub = make_email_validator_stub(is_valid=False)
        add_account_stub = make_add_account_stub()
        sut = SignUpController(email_validator_stub, add_account_stub)
        http_request = HttpRequest({
            "name": "any_name",
            "email": "invalid_email",
            "password": "Valid_password123",
            "passwordConfirmation": "Valid_password123"
        })

        http_response = sut.handle(http_request)

        self.assertEqual(http_response.status_code, 400)
        self.assertIsInstance(http_response.body, InvalidParamError)
        self.assertEqual(str(http_response.body), "Invalid param: email")

    def test_should_return_403_if_email_is_already_in_use(self):
        email_validator_stub = make_email_validator_stub()

        class AddAccountStubDuplicatedEmail(AddAccount):
            async def add(self, account: AddAccountModel):
                return None

        sut = SignUpController(email_validator_stub, AddAccountStubDuplicatedEmail())
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "Valid_password123",
            "passwordConfirmation": "Valid_password123"
        })

        http_response = sut.handle(http_request)

        self.assertEqual(http_response.status_code, 403)
        self.assertIsInstance(http_response.body, EmailInUseError)
        self.assertEqual(str(http_response.body), "Email already in use")

    def test_should_return_200_if_all_data_is_valid(self):
        sut = make_sut()
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "Valid_password123",
            "passwordConfirmation": "Valid_password123"
        })
        http_response = sut.handle(http_request)
        self.assertEqual(http_response.status_code, 200)
        self.assertEqual(http_response.body.id, "valid_id")
        self.assertEqual(http_response.body.name, "valid_name")
        self.assertEqual(http_response.body.email, "valid_email@mail.com")
        self.assertEqual(http_response.body.password, "Valid_password123")

    def test_should_return_400_if_password_is_weak(self):
        sut = make_sut()
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "password",
            "passwordConfirmation": "password"
        })
        http_response = sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertIsInstance(http_response.body, InvalidParamError)
        self.assertEqual(str(http_response.body), "Invalid param: password")

    def test_should_return_500_if_add_account_throws(self):
        email_validator_stub = make_email_validator_stub()
        
        class AddAccountStubWithError(AddAccount):
            async def add(self, account: AddAccountModel) -> AccountModel:
                raise Exception("Database error")
        
        add_account_stub = AddAccountStubWithError()
        sut = SignUpController(email_validator_stub, add_account_stub)
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "Valid_password123",
            "passwordConfirmation": "Valid_password123"
        })
        http_response = sut.handle(http_request)
        self.assertEqual(http_response.status_code, 500)
        self.assertIsInstance(http_response.body, ServerError)

    def test_should_call_add_account_with_correct_values(self):
        email_validator_stub = make_email_validator_stub()
        add_account_spy = Mock(spec=AddAccount)
        async def mock_add(account):
            return AccountModel(
                id="valid_id",
                name="valid_name",
                email="valid_email@mail.com",
                password="Valid_password123"
            )
        add_account_spy.add = AsyncMock(side_effect=mock_add)
        sut = SignUpController(email_validator_stub, add_account_spy)
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "Valid_password123",
            "passwordConfirmation": "Valid_password123"
        })
        sut.handle(http_request)
        add_account_spy.add.assert_called_once_with(AddAccountModel(
            name="any_name",
            email="any_email@mail.com",
            password="Valid_password123"
        ))

    def test_should_authenticate_after_account_creation_and_return_token(self):
        validation_stub = Mock()
        validation_stub.validate.return_value = None
        add_account_spy = Mock(spec=AddAccount)
        add_account_spy.add = AsyncMock(return_value=AccountModel(
            id="valid_id",
            name="any_name",
            email="any_email@mail.com",
            password="hashed_password"
        ))
        authentication_spy = Mock()
        authentication_spy.auth = AsyncMock(return_value=AuthenticationModel(
            access_token="generated_token",
            name="any_name",
        ))
        sut = SignUpController(add_account_spy, validation_stub, authentication_spy)
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "Valid_password123",
            "passwordConfirmation": "Valid_password123"
        })

        http_response = sut.handle(http_request)

        self.assertEqual(http_response.status_code, 200)
        self.assertEqual(http_response.body.access_token, "generated_token")
        self.assertEqual(http_response.body.name, "any_name")
        authentication_spy.auth.assert_called_once()
        auth_params = authentication_spy.auth.call_args.args[0]
        self.assertEqual(auth_params.email, "any_email@mail.com")
        self.assertEqual(auth_params.password, "Valid_password123")

    def test_should_return_500_if_authentication_throws_after_account_creation(self):
        validation_stub = Mock()
        validation_stub.validate.return_value = None
        add_account_spy = Mock(spec=AddAccount)
        add_account_spy.add = AsyncMock(return_value=AccountModel(
            id="valid_id",
            name="any_name",
            email="any_email@mail.com",
            password="hashed_password"
        ))
        authentication_spy = Mock()
        authentication_spy.auth = AsyncMock(side_effect=Exception("Auth error"))
        sut = SignUpController(add_account_spy, validation_stub, authentication_spy)
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "Valid_password123",
            "passwordConfirmation": "Valid_password123"
        })

        http_response = sut.handle(http_request)

        self.assertEqual(http_response.status_code, 500)
        self.assertIsInstance(http_response.body, ServerError)


if __name__ == '__main__':
    unittest.main()
