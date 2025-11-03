from email_validator import validate_email, EmailNotValidError
from presentation.protocols.email_validator import EmailValidator


class EmailValidatorAdapter(EmailValidator):
    def is_valid(self, email: str) -> bool:
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False

