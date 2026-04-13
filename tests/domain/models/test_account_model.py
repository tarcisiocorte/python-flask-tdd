from dataclasses import fields

from domain.models.account import AccountModel


def test_should_create_account_model_with_valid_data() -> None:
    account = AccountModel(
        id="account_123",
        name="Alice",
        email="alice@example.com",
        password="hashed_password_abc",
    )

    assert account.id == "account_123"
    assert account.name == "Alice"
    assert account.email == "alice@example.com"
    assert account.password == "hashed_password_abc"


def test_should_define_expected_account_field_types() -> None:
    field_types = {field.name: field.type for field in fields(AccountModel)}

    assert field_types == {
        "id": str,
        "name": str,
        "email": str,
        "password": str,
    }
