import bcrypt
from data.protocols.encrypter import Encrypter


class BcryptAdapter(Encrypter):
    def __init__(self, salt: int):
        self._salt = salt

    async def encrypt(self, value: str) -> str:
        salt = bcrypt.gensalt(rounds=self._salt)
        hashed = bcrypt.hashpw(value.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    async def compare(self, value: str, hash: str) -> bool:
        return bcrypt.checkpw(value.encode('utf-8'),hash.encode('utf-8'))

