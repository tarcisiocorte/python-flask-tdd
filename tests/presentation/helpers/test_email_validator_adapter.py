import unittest
from unittest.mock import patch, MagicMock
from presentation.helpers.email_validator_adapter import EmailValidatorAdapter


class TestEmailValidatorAdapter(unittest.TestCase):
    def test_should_return_false_if_email_is_invalid(self):
        sut = EmailValidatorAdapter()
        is_valid = sut.is_valid('invalid_email')
        self.assertFalse(is_valid)

    def test_should_return_false_if_email_is_empty(self):
        sut = EmailValidatorAdapter()
        is_valid = sut.is_valid('')
        self.assertFalse(is_valid)

    def test_should_return_false_if_email_has_no_at_symbol(self):
        sut = EmailValidatorAdapter()
        is_valid = sut.is_valid('invalidemail.com')
        self.assertFalse(is_valid)

    def test_should_return_false_if_email_has_no_domain(self):
        sut = EmailValidatorAdapter()
        is_valid = sut.is_valid('invalid@')
        self.assertFalse(is_valid)

    def test_should_return_true_if_email_is_valid(self):
        sut = EmailValidatorAdapter()
        is_valid = sut.is_valid('valid@example.com')
        self.assertTrue(is_valid)

    def test_should_return_true_if_email_has_subdomain(self):
        sut = EmailValidatorAdapter()
        is_valid = sut.is_valid('user@mail.example.com')
        self.assertTrue(is_valid)

    def test_should_return_false_if_validator_returns_false(self):
        sut = EmailValidatorAdapter()
        
        with patch('presentation.helpers.email_validator_adapter.validate_email') as mock_validate:
            from email_validator import EmailNotValidError
            mock_validate.side_effect = EmailNotValidError('Validation failed')  # Mock validator returning false
            is_valid = sut.is_valid('invalid_email@mail.com')
            self.assertFalse(is_valid)

    def test_should_return_true_if_validator_returns_true(self):
        sut = EmailValidatorAdapter()
        
        with patch('presentation.helpers.email_validator_adapter.validate_email') as mock_validate:
            mock_validate.return_value = True  # Mock validator returning true
            is_valid = sut.is_valid('valid_email@mail.com')
            self.assertTrue(is_valid)


if __name__ == '__main__':
    unittest.main()
