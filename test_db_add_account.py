import unittest
from unittest.mock import AsyncMock, patch
from infrastructure.db_add_account import DbAddAccount
from domain.usecases.add_account import AddAccountModel


class EncrypterStub:
    async def encrypt(self, value: str) -> str:
        # Use the value parameter to avoid linting warning
        return f"hashed_{value}"


class TestDbAddAccount(unittest.TestCase):
    def test_should_call_encrypter_with_correct_password(self):
        # Arrange
        encrypter_stub = EncrypterStub()
        sut = DbAddAccount(encrypter_stub)
        
        # Mock the encrypt method to track calls
        with patch.object(encrypter_stub, 'encrypt', new_callable=AsyncMock) as encrypt_spy:
            account_data = AddAccountModel(
                name="valid_name",
                email="valid_email",
                password="valid_password"
            )
            
            # Act
            import asyncio
            asyncio.run(sut.add(account_data))
            
            # Assert
            encrypt_spy.assert_called_once_with("valid_password")


if __name__ == '__main__':
    unittest.main()
