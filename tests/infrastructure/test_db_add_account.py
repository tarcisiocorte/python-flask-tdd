import unittest
import asyncio
from unittest.mock import AsyncMock, patch
from infrastructure.db_add_account import DbAddAccount
from domain.usecases.add_account import AddAccountModel
from protocols.encrypter import Encrypter
from typing import NamedTuple


class EncrypterStub(Encrypter):
    async def encrypt(self, value: str) -> str:
        return "hashed_password"


class SutTypes(NamedTuple):
    sut: DbAddAccount
    encrypter_stub: EncrypterStub


def make_sut() -> SutTypes:
    encrypter_stub = EncrypterStub()
    sut = DbAddAccount(encrypter_stub)
    return SutTypes(
        sut=sut,
        encrypter_stub=encrypter_stub
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


if __name__ == '__main__':
    unittest.main()
