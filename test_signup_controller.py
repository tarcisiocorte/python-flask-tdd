import unittest
from unittest.mock import Mock
from signup import SignUpController
from protocols.http import HttpRequest
from domain.usecases.add_account import AddAccount, AddAccountModel
from domain.models.account import AccountModel
from errors.server_error import ServerError


def make_add_account_stub() -> AddAccount:
    class AddAccountStub(AddAccount):
        def add(self, account: AddAccountModel) -> AccountModel:
            return AccountModel(
                id="valid_id",
                name="valid_name",
                email="valid_email@mail.com",
                password="valid_password"
            )
    return AddAccountStub()


def make_sut() -> SignUpController:
    add_account_stub = make_add_account_stub()
    return SignUpController(add_account_stub)


class TestSignUpController(unittest.TestCase):
    def test_should_return_400_if_no_name_provided(self):
        sut = make_sut()
        http_request = HttpRequest({
            "email": "any_email@mail.com",
            "password": "any_password",
            "passwordConfirmation": "any_password"
        })
        http_response = sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.body, {"error": "Missing param: name"})

    def test_should_return_400_if_no_email_provided(self):
        sut = make_sut()
        http_request = HttpRequest({
            "name": "any_name",
            "password": "any_password",
            "passwordConfirmation": "any_password"
        })
        http_response = sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.body, {"error": "Missing param: email"})

    def test_should_return_400_if_no_password_provided(self):
        sut = make_sut()
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "passwordConfirmation": "any_password"
        })
        http_response = sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.body, {"error": "Missing param: password"})

    def test_should_return_400_if_no_password_confirmation_provided(self):
        sut = make_sut()
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "any_password"
        })
        http_response = sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.body, {"error": "Missing param: passwordConfirmation"})

    def test_should_return_400_if_password_confirmation_fails(self):
        sut = make_sut()
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "any_password",
            "passwordConfirmation": "invalid_confirmation"
        })
        http_response = sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.body, {"error": "Password confirmation does not match password"})

    def test_should_return_200_if_all_data_is_valid(self):
        sut = make_sut()
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "any_password",
            "passwordConfirmation": "any_password"
        })
        http_response = sut.handle(http_request)
        self.assertEqual(http_response.status_code, 200)
        self.assertEqual(http_response.body, {
            "id": "valid_id",
            "name": "valid_name",
            "email": "valid_email@mail.com",
            "password": "valid_password"
        })

    def test_should_return_500_if_add_account_throws(self):
        add_account_stub = Mock(spec=AddAccount)
        add_account_stub.add.side_effect = Exception("Database error")
        sut = SignUpController(add_account_stub)
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "any_password",
            "passwordConfirmation": "any_password"
        })
        http_response = sut.handle(http_request)
        self.assertEqual(http_response.status_code, 500)
        self.assertEqual(http_response.body, {"error": "Internal server error"})

    def test_should_call_add_account_with_correct_values(self):
        add_account_spy = Mock(spec=AddAccount)
        add_account_spy.add.return_value = AccountModel(
            id="valid_id",
            name="valid_name",
            email="valid_email@mail.com",
            password="valid_password"
        )
        sut = SignUpController(add_account_spy)
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "any_password",
            "passwordConfirmation": "any_password"
        })
        sut.handle(http_request)
        add_account_spy.add.assert_called_once_with(AddAccountModel(
            name="any_name",
            email="any_email@mail.com",
            password="any_password"
        ))


if __name__ == '__main__':
    unittest.main()
