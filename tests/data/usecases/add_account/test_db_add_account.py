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

    async def compare(self, value: str, hash: str) -> bool:
        return value == hash


class AddAccountRepositoryStub(AddAccountRepository):
    async def add(self, account: AddAccountModel) -> AccountModel:
        return AccountModel(
            id="valid_id",
            name=account.name,
            email=account.email,
            password=account.password
        )


class CheckAccountByEmailRepositoryStub:
    def __init__(self, exists: bool = False):
        self.exists = exists
        self.emails = []

    async def check_by_email(self, email: str) -> bool:
        self.emails.append(email)
        return self.exists


class SutTypes(NamedTuple):
    sut: DbAddAccount
    encrypter_stub: EncrypterStub
    add_account_repository_stub: AddAccountRepositoryStub
    check_account_by_email_repository_stub: CheckAccountByEmailRepositoryStub


def make_sut(account_exists: bool = False) -> SutTypes:
    encrypter_stub = EncrypterStub()
    add_account_repository_stub = AddAccountRepositoryStub()
    check_account_by_email_repository_stub = CheckAccountByEmailRepositoryStub(
        account_exists
    )
    sut = DbAddAccount(
        encrypter_stub,
        add_account_repository_stub,
        check_account_by_email_repository_stub,
    )
    return SutTypes(
        sut=sut,
        encrypter_stub=encrypter_stub,
        add_account_repository_stub=add_account_repository_stub,
        check_account_by_email_repository_stub=check_account_by_email_repository_stub,
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

    def test_should_return_an_account_on_success(self):
        sut_types = make_sut()
        sut = sut_types.sut
        add_account_repository_stub = sut_types.add_account_repository_stub

        with patch.object(add_account_repository_stub, 'add', return_value=AccountModel(
            id="valid_id",
            name="valid_name",
            email="valid_email",
            password="hashed_password"
        )):
            account_data = AddAccountModel(
                name="valid_name",
                email="valid_email",
                password="valid_password"
            )
            account = asyncio.run(sut.add(account_data))
            self.assertEqual(account.id, "valid_id")
            self.assertEqual(account.name, "valid_name")
            self.assertEqual(account.email, "valid_email")
            self.assertEqual(account.password, "hashed_password")

    def test_should_check_email_before_creating_account(self):
        sut_types = make_sut()
        sut = sut_types.sut
        checker_stub = sut_types.check_account_by_email_repository_stub

        account_data = AddAccountModel(
            name="valid_name",
            email="valid_email",
            password="valid_password"
        )

        asyncio.run(sut.add(account_data))

        self.assertEqual(checker_stub.emails, ["valid_email"])

    def test_should_return_none_without_hashing_or_inserting_if_email_exists(self):
        sut_types = make_sut(account_exists=True)
        sut = sut_types.sut
        encrypter_stub = sut_types.encrypter_stub
        add_account_repository_stub = sut_types.add_account_repository_stub

        with patch.object(encrypter_stub, 'encrypt', new_callable=AsyncMock) as encrypt_spy:
            with patch.object(
                add_account_repository_stub,
                'add',
                new_callable=AsyncMock,
            ) as add_spy:
                account_data = AddAccountModel(
                    name="valid_name",
                    email="valid_email",
                    password="valid_password"
                )

                account = asyncio.run(sut.add(account_data))

                self.assertIsNone(account)
                encrypt_spy.assert_not_called()
                add_spy.assert_not_called()

    def test_should_throw_if_add_account_repository_throws(self):
        sut_types = make_sut()
        sut = sut_types.sut
        add_account_repository_stub = sut_types.add_account_repository_stub

        with patch.object(add_account_repository_stub, 'add', side_effect=Exception) as add_spy:
            account_data = AddAccountModel(
                name="valid_name",
                email="valid_email",
                password="valid_password"
            )
            with self.assertRaises(Exception):
                asyncio.run(sut.add(account_data))
            add_spy.assert_called_once_with(AddAccountModel(
                name="valid_name",
                email="valid_email",
                password="hashed_password"
            ))


if __name__ == '__main__':
    unittest.main()
