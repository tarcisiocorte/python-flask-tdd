import pytest
from signup import SignUpController

def test_should_return_400_if_no_name_provided():
    sut = SignUpController()
    http_request = {
        "body": {
            "email": "any_email@mail.com",
            "password": "any_password",
            "passwordConfirmation": "any_password"
        }
    }
    http_response = sut.handle(http_request)
    assert http_response["statusCode"] == 400