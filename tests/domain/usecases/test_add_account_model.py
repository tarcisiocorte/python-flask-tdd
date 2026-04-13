from dataclasses import fields

from domain.usecases.add_account import AddAccountModel


def test_should_create_add_account_model_with_valid_data() -> None:
    account = AddAccountModel(
        name="Alice",
        email="alice@example.com",
        password="plain_password_123",
    )

    assert account.name == "Alice"
    assert account.email == "alice@example.com"
    assert account.password == "plain_password_123"


def test_should_define_expected_add_account_field_types() -> None:
    field_types = {field.name: field.type for field in fields(AddAccountModel)}

    assert field_types == {
        "name": str,
        "email": str,
        "password": str,
    }
