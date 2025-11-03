import bcrypt
from data.protocols.encrypter import Encrypter


class BcryptEncrypter(Encrypter):
    async def encrypt(self, value: str) -> str:
        # Generate salt and hash the password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(value.encode('utf-8'), salt)
        return hashed.decode('utf-8')

