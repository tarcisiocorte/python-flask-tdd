import unittest
import asyncio
from unittest.mock import AsyncMock, patch, Mock
from data.usecases.add_account.db_add_account import DbAddAccount
from domain.usecases.add_account import AddAccountModel
from domain.models.account import AccountModel
from data.protocols.encrypter import Encrypter
from data.protocols.add_account_repository import AddAccountRepository
from typing import NamedTuple


class EncrypterStub(Encrypter):
    async def encrypt(self, value: str) -> str:
        return "hashed_password"


class AddAccountRepositoryStub(AddAccountRepository):
    async def add(self, account: AddAccountModel) -> AccountModel:
        return AccountModel(
            id="valid_id",
            name=account.name,
            email=account.email,
            password=account.password
        )


class SutTypes(NamedTuple):
    sut: DbAddAccount
    encrypter_stub: EncrypterStub
    add_account_repository_stub: AddAccountRepositoryStub


def make_sut() -> SutTypes:
    encrypter_stub = EncrypterStub()
    add_account_repository_stub = AddAccountRepositoryStub()
    sut = DbAddAccount(encrypter_stub, add_account_repository_stub)
    return SutTypes(
        sut=sut,
        encrypter_stub=encrypter_stub,
        add_account_repository_stub=add_account_repository_stub
    )


class TestDbAddAccount(unittest.TestCase):
    def test_should_call_encrypter_with_correct_password(self):
        sut_types = make_sut()
        sut = sut_types.sut
        encrypter_stub = sut_types.encrypter_stub

        with patch.object(encrypter_stub, 'encrypt', new_callable=AsyncMock) as encrypt_spy:
            account_data = AddAccountModel(
                name="valid_name",
                email="valid_email",
                password="valid_password"
            )

            asyncio.run(sut.add(account_data))

            encrypt_spy.assert_called_once_with("valid_password")

    def test_should_throw_if_encrypter_throws(self):
        sut_types = make_sut()
        sut = sut_types.sut
        encrypter_stub = sut_types.encrypter_stub

        with patch.object(encrypter_stub, 'encrypt', side_effect=Exception) as encrypt_spy:
            account_data = AddAccountModel(
                name="valid_name",
                email="valid_email",
                password="valid_password"
            )

            with self.assertRaises(Exception):
                asyncio.run(sut.add(account_data))

            encrypt_spy.assert_called_once_with("valid_password")
            
    def test_should_call_add_account_repository_with_correct_values(self):
        sut_types = make_sut()
        sut = sut_types.sut
        add_account_repository_stub = sut_types.add_account_repository_stub

        with patch.object(add_account_repository_stub, 'add', new_callable=AsyncMock) as add_spy:
            account_data = AddAccountModel(
                name="valid_name",
                email="valid_email",
                password="valid_password"
            )

            asyncio.run(sut.add(account_data))

            expected_account_data = AddAccountModel(
                name="valid_name",
                email="valid_email",
                password="hashed_password"
            )
            add_spy.assert_called_once_with(expected_account_data)   


if __name__ == '__main__':
    unittest.main()
