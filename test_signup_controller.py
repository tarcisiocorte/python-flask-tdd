import pytest
from signup import SignUpController

@pytest.fixture
def sut():
    return SignUpController()

def test_should_return_400_if_no_name_provided(sut):
    http_request = {
        "body": {
            "email": "any_email@mail.com",
            "password": "any_password",
            "passwordConfirmation": "any_password"
        }
    }
    http_response = sut.handle(http_request)
    assert http_response["statusCode"] == 400
    assert http_response["body"] == {"error": "Missing param: name"}

def test_should_return_400_if_no_email_provided(sut):
    http_request = {
        "body": {
            "name": "any_name",
            "password": "any_password",
            "passwordConfirmation": "any_password"
        }
    }
    http_response = sut.handle(http_request)
    assert http_response["statusCode"] == 400
    assert http_response["body"] == {"error": "Missing param: email"}

def test_should_return_400_if_no_password_provided(sut):
    http_request = {
        "body": {
            "name": "any_name",
            "email": "any_email@mail.com",
            "passwordConfirmation": "any_password"
        }
    }
    http_response = sut.handle(http_request)
    assert http_response["statusCode"] == 400
    assert http_response["body"] == {"error": "Missing param: password"}

def test_should_return_400_if_no_password_confirmation_provided(sut):
    http_request = {
        "body": {
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "any_password"
        }
    }
    http_response = sut.handle(http_request)
    assert http_response["statusCode"] == 400
    assert http_response["body"] == {"error": "Missing param: passwordConfirmation"}

def test_should_return_400_if_password_confirmation_fails(sut):
    http_request = {
        "body": {
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "any_password",
            "passwordConfirmation": "invalid_confirmation"
        }
    }
    http_response = sut.handle(http_request)
    assert http_response["statusCode"] == 400
    assert http_response["body"] == {"error": "Password confirmation does not match password"}

def test_should_return_200_if_all_data_is_valid(sut):
    http_request = {
        "body": {
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "any_password",
            "passwordConfirmation": "any_password"
        }
    }
    http_response = sut.handle(http_request)
    assert http_response["statusCode"] == 200
    assert http_response["body"] == {"message": "User signed up successfully"}
