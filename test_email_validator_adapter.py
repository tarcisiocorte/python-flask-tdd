import unittest
from presentation.helpers.email_validator_adapter import EmailValidatorAdapter


class TestEmailValidatorAdapter(unittest.TestCase):
    def test_should_return_false_if_validator_returns_false(self):
        sut = EmailValidatorAdapter()
        is_valid = sut.is_valid('invalid_email@mail.com')
        self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()
