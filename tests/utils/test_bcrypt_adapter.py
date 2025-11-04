import unittest
import asyncio
from unittest.mock import patch, MagicMock
from infra.criptography.bcrypt_adapter import BcryptAdapter


def make_sut(salt: int = 12) -> BcryptAdapter:
    return BcryptAdapter(salt)


class TestBcryptAdapter(unittest.TestCase):
    def test_should_call_bcrypt_with_correct_values(self):
        salt = 12
        sut = make_sut(salt)
        
        with patch('infra.criptography.bcrypt_adapter.bcrypt') as bcrypt_mock:
            # Mock gensalt to return a bytes salt
            bcrypt_mock.gensalt.return_value = b'$2b$12$test_salt_value_here'
            # Mock hashpw to return a bytes hash
            bcrypt_mock.hashpw.return_value = b'$2b$12$hashed_value'
            
            asyncio.run(sut.encrypt('any_value'))
            
            # Verify gensalt was called with correct rounds
            bcrypt_mock.gensalt.assert_called_once_with(rounds=salt)
            
            # Verify hashpw was called with encoded password and salt
            bcrypt_mock.hashpw.assert_called_once_with(
                'any_value'.encode('utf-8'),
                bcrypt_mock.gensalt.return_value
            )


if __name__ == '__main__':
    unittest.main()

