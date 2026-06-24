from __future__ import annotations

import asyncio
from dataclasses import dataclass

from data.usecases.authentication import DbAuthentication
from domain.models.account import AccountModel
from domain.usecases import AuthenticationParams


class LoadAccountByEmailRepositoryStub:
    async def load_by_email(self, email: str):
        if email != "valid_email@mail.com":
            return None
        return AccountModel(
            id="account_id",
            name="Valid User",
            email=email,
            password="hashed_password",
        )


class HashComparerStub:
    def __init__(self, is_valid: bool = True):
        self.is_valid = is_valid
        self.calls = []

    async def compare(self, value: str, digest: str) -> bool:
        self.calls.append((value, digest))
        return self.is_valid


class EncrypterStub:
    def __init__(self):
        self.calls = []

    async def encrypt(self, value: str) -> str:
        self.calls.append(value)
        return "generated_token"


@dataclass
class UpdateAccessTokenRepositorySpy:
    account_id: str | None = None
    token: str | None = None

    async def update_access_token(self, account_id: str, token: str) -> None:
        self.account_id = account_id
        self.token = token


def make_sut(is_valid_password: bool = True):
    load_account_by_email_repository = LoadAccountByEmailRepositoryStub()
    hash_comparer = HashComparerStub(is_valid_password)
    encrypter = EncrypterStub()
    update_access_token_repository = UpdateAccessTokenRepositorySpy()
    sut = DbAuthentication(
        load_account_by_email_repository,
        hash_comparer,
        encrypter,
        update_access_token_repository,
    )
    return sut, hash_comparer, encrypter, update_access_token_repository


def test_authentication_returns_access_token_and_name_on_success():
    sut, hash_comparer, encrypter, update_access_token_repository = make_sut()

    authentication = asyncio.run(
        sut.auth(AuthenticationParams("valid_email@mail.com", "valid_password"))
    )

    assert authentication.access_token == "generated_token"
    assert authentication.name == "Valid User"
    assert hash_comparer.calls == [("valid_password", "hashed_password")]
    assert encrypter.calls == ["account_id"]
    assert update_access_token_repository.account_id == "account_id"
    assert update_access_token_repository.token == "generated_token"


def test_authentication_returns_none_for_invalid_email():
    sut, _, _, update_access_token_repository = make_sut()

    authentication = asyncio.run(
        sut.auth(AuthenticationParams("invalid_email@mail.com", "valid_password"))
    )

    assert authentication is None
    assert update_access_token_repository.account_id is None
    assert update_access_token_repository.token is None


def test_authentication_returns_none_for_invalid_password():
    sut, _, _, update_access_token_repository = make_sut(is_valid_password=False)

    authentication = asyncio.run(
        sut.auth(AuthenticationParams("valid_email@mail.com", "invalid_password"))
    )

    assert authentication is None
    assert update_access_token_repository.account_id is None
    assert update_access_token_repository.token is None
