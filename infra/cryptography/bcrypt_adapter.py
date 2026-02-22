import bcrypt
from data.protocols.encrypter import Encrypter


class BcryptAdapter(Encrypter):
    def __init__(self, salt: int):
        self._salt = salt

    async def encrypt(self, value: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt(rounds=self._salt)
        hashed = bcrypt.hashpw(value.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    async def compare(self, value: str, hash: str) -> bool:
        """Compare a plain text value with a bcrypt hash."""
        return bcrypt.checkpw(value.encode('utf-8'), hash.encode('utf-8'))

