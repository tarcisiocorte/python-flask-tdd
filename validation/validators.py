from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from presentation.errors import InvalidParamError, MissingParamError
from presentation.protocols import Validation
from validation.protocols import EmailValidator


def _get(input_data: Any, field: str) -> Any:
    if isinstance(input_data, dict):
        return input_data.get(field)
    return getattr(input_data, field, None)


@dataclass
class RequiredFieldValidation(Validation):
    field_name: str

    def validate(self, input_data: Any) -> Exception | None:
        return None if _get(input_data, self.field_name) else MissingParamError(self.field_name)


@dataclass
class CompareFieldsValidation(Validation):
    field_name: str
    field_to_compare: str

    def validate(self, input_data: Any) -> Exception | None:
        if _get(input_data, self.field_name) != _get(input_data, self.field_to_compare):
            return InvalidParamError(self.field_to_compare)
        return None


@dataclass
class EmailValidation(Validation):
    field_name: str
    email_validator: EmailValidator

    def validate(self, input_data: Any) -> Exception | None:
        email = _get(input_data, self.field_name)
        if email and not self.email_validator.is_valid(email):
            return InvalidParamError(self.field_name)
        return None


@dataclass
class PasswordStrengthValidation(Validation):
    field_name: str
    min_length: int = 8

    def validate(self, input_data: Any) -> Exception | None:
        password = _get(input_data, self.field_name)
        if not password:
            return None
        has_lower = any(character.islower() for character in password)
        has_upper = any(character.isupper() for character in password)
        has_digit = any(character.isdigit() for character in password)
        if len(password) < self.min_length or not (has_lower and has_upper and has_digit):
            return InvalidParamError(self.field_name)
        return None


class ValidationComposite(Validation):
    def __init__(self, validations: Iterable[Validation]):
        self.validations = list(validations)

    def validate(self, input_data: Any) -> Exception | None:
        for validation in self.validations:
            error = validation.validate(input_data)
            if error:
                return error
        return None
