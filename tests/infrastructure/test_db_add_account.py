import unittest
import asyncio
from unittest.mock import AsyncMock, patch
from infrastructure.db_add_account import DbAddAccount
from domain.usecases.add_account import AddAccountModel


class EncrypterStub:
    async def encrypt(self, value: str) -> str:
        return "hashed_password"


class TestDbAddAccount(unittest.TestCase):
    def test_should_call_encrypter_with_correct_password(self):

        encrypter_stub = EncrypterStub()
        sut = DbAddAccount(encrypter_stub)

        with patch.object(encrypter_stub, 'encrypt', new_callable=AsyncMock) as encrypt_spy:
            account_data = AddAccountModel(
                name="valid_name",
                email="valid_email",
                password="valid_password"
            )

            asyncio.run(sut.add(account_data))

            encrypt_spy.assert_called_once_with("valid_password")


if __name__ == '__main__':
    unittest.main()
