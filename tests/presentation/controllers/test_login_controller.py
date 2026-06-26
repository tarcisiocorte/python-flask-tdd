from unittest.mock import AsyncMock, Mock

from domain.usecases import AuthenticationModel
from presentation.controllers.login_controller import LoginController
from presentation.errors import InvalidParamError, MissingParamError, UnauthorizedError
from presentation.errors.server_error import ServerError
from presentation.protocols.http import HttpRequest


def make_sut(validation_error=None, authentication_result=None):
    authentication = Mock()
    authentication.auth = AsyncMock(return_value=authentication_result)
    validation = Mock()
    validation.validate.return_value = validation_error
    sut = LoginController(authentication, validation)
    return sut, authentication, validation


def test_login_returns_400_if_email_is_missing():
    sut, authentication, _ = make_sut(MissingParamError("email"))

    response = sut.handle(HttpRequest({"password": "Valid_password123"}))

    assert response.status_code == 400
    assert isinstance(response.body, MissingParamError)
    assert str(response.body) == "Missing param: email"
    authentication.auth.assert_not_called()


def test_login_returns_400_if_password_is_missing():
    sut, authentication, _ = make_sut(MissingParamError("password"))

    response = sut.handle(HttpRequest({"email": "any_email@mail.com"}))

    assert response.status_code == 400
    assert isinstance(response.body, MissingParamError)
    assert str(response.body) == "Missing param: password"
    authentication.auth.assert_not_called()


def test_login_returns_400_if_email_is_invalid():
    sut, authentication, _ = make_sut(InvalidParamError("email"))

    response = sut.handle(HttpRequest({
        "email": "invalid_email",
        "password": "Valid_password123",
    }))

    assert response.status_code == 400
    assert isinstance(response.body, InvalidParamError)
    assert str(response.body) == "Invalid param: email"
    authentication.auth.assert_not_called()


def test_login_calls_authentication_with_email_and_password():
    sut, authentication, _ = make_sut(authentication_result=AuthenticationModel(
        access_token="generated_token",
        name="Valid User",
    ))
    request = HttpRequest({
        "email": "valid_email@mail.com",
        "password": "Valid_password123",
    })

    sut.handle(request)

    authentication.auth.assert_called_once_with({
        "email": "valid_email@mail.com",
        "password": "Valid_password123",
    })


def test_login_returns_401_if_authentication_fails():
    sut, _, _ = make_sut(authentication_result=None)

    response = sut.handle(HttpRequest({
        "email": "valid_email@mail.com",
        "password": "wrong_password",
    }))

    assert response.status_code == 401
    assert isinstance(response.body, UnauthorizedError)


def test_login_returns_auth_response_on_success():
    sut, _, _ = make_sut(authentication_result=AuthenticationModel(
        access_token="generated_token",
        name="Valid User",
    ))

    response = sut.handle(HttpRequest({
        "email": "valid_email@mail.com",
        "password": "Valid_password123",
    }))

    assert response.status_code == 200
    assert response.body.access_token == "generated_token"
    assert response.body.name == "Valid User"


def test_login_returns_500_if_authentication_throws():
    sut, authentication, _ = make_sut()
    authentication.auth = AsyncMock(side_effect=Exception("auth error"))

    response = sut.handle(HttpRequest({
        "email": "valid_email@mail.com",
        "password": "Valid_password123",
    }))

    assert response.status_code == 500
    assert isinstance(response.body, ServerError)
