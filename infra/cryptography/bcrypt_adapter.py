import bcrypt
from data.protocols.encrypter import Encrypter, HashComparer, Hasher


class BcryptAdapter(Encrypter, Hasher, HashComparer):
    def __init__(self, salt: int):
        self._salt = salt

    async def hash(self, value: str) -> str:
        return await self.encrypt(value)

    async def encrypt(self, value: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt(rounds=self._salt)
        hashed = bcrypt.hashpw(value.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    async def compare(self, value: str, digest: str) -> bool:
        """Compare a plain text value with a bcrypt hash."""
        return bcrypt.checkpw(value.encode('utf-8'), digest.encode('utf-8'))
