import unittest
from unittest.mock import patch, MagicMock
from utils.email_validator_adapter import EmailValidatorAdapter


def make_sut() -> EmailValidatorAdapter:
    return EmailValidatorAdapter()


class TestEmailValidatorAdapter(unittest.TestCase):
    def test_should_return_false_if_email_is_invalid(self):
        sut = make_sut()
        is_valid = sut.is_valid('invalid_email')
        self.assertFalse(is_valid)

    def test_should_return_false_if_email_is_empty(self):
        sut = make_sut()
        is_valid = sut.is_valid('')
        self.assertFalse(is_valid)

    def test_should_return_false_if_email_has_no_at_symbol(self):
        sut = make_sut()
        is_valid = sut.is_valid('invalidemail.com')
        self.assertFalse(is_valid)

    def test_should_return_false_if_email_has_no_domain(self):
        sut = make_sut()
        is_valid = sut.is_valid('invalid@')
        self.assertFalse(is_valid)

    def test_should_return_true_if_email_is_valid(self):
        sut = make_sut()
        is_valid = sut.is_valid('valid@example.com')
        self.assertTrue(is_valid)

    def test_should_return_true_if_email_has_subdomain(self):
        sut = make_sut()
        is_valid = sut.is_valid('user@mail.example.com')
        self.assertTrue(is_valid)

    def test_should_return_false_if_validator_returns_false(self):
        sut = make_sut()
        
        with patch('utils.email_validator_adapter.validate_email') as mock_validate:
            from email_validator import EmailNotValidError
            mock_validate.side_effect = EmailNotValidError('Validation failed')
            is_valid = sut.is_valid('invalid_email@mail.com')
            self.assertFalse(is_valid)

    def test_should_return_true_if_validator_returns_true(self):
        sut = make_sut()
        
        with patch('utils.email_validator_adapter.validate_email') as mock_validate:
            mock_validate.return_value = True
            is_valid = sut.is_valid('valid_email@mail.com')
            self.assertTrue(is_valid)

    def test_should_call_validator_with_correct_email(self):
        sut = make_sut()
        with patch('utils.email_validator_adapter.validate_email') as mock_validate:
            sut.is_valid('any_email@mail.com')
            mock_validate.assert_called_once_with('any_email@mail.com', check_deliverability=False)


if __name__ == '__main__':
    unittest.main()
