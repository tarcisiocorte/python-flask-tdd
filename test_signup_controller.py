import unittest
from signup import SignUpController
from protocols.http import HttpRequest


class TestSignUpController(unittest.TestCase):
    def setUp(self):
        self.sut = SignUpController()

    def test_should_return_400_if_no_name_provided(self):
        http_request = HttpRequest({
            "email": "any_email@mail.com",
            "password": "any_password",
            "passwordConfirmation": "any_password"
        })
        http_response = self.sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.body, {"error": "Missing param: name"})

    def test_should_return_400_if_no_email_provided(self):
        http_request = HttpRequest({
            "name": "any_name",
            "password": "any_password",
            "passwordConfirmation": "any_password"
        })
        http_response = self.sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.body, {"error": "Missing param: email"})

    def test_should_return_400_if_no_password_provided(self):
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "passwordConfirmation": "any_password"
        })
        http_response = self.sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.body, {"error": "Missing param: password"})

    def test_should_return_400_if_no_password_confirmation_provided(self):
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "any_password"
        })
        http_response = self.sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.body, {"error": "Missing param: passwordConfirmation"})

    def test_should_return_400_if_password_confirmation_fails(self):
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "any_password",
            "passwordConfirmation": "invalid_confirmation"
        })
        http_response = self.sut.handle(http_request)
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.body, {"error": "Password confirmation does not match password"})

    def test_should_return_200_if_all_data_is_valid(self):
        http_request = HttpRequest({
            "name": "any_name",
            "email": "any_email@mail.com",
            "password": "any_password",
            "passwordConfirmation": "any_password"
        })
        http_response = self.sut.handle(http_request)
        self.assertEqual(http_response.status_code, 200)
        self.assertEqual(http_response.body, {"message": "User signed up successfully"})


if __name__ == '__main__':
    unittest.main()
