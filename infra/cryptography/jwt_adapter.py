from __future__ import annotations

import jwt

from data.protocols.encrypter import Decrypter, Encrypter


class JwtAdapter(Encrypter, Decrypter):
    def __init__(self, secret: str):
        self.secret = secret

    async def encrypt(self, value: str) -> str:
        return jwt.encode({"id": value}, self.secret, algorithm="HS256")

    async def decrypt(self, value: str) -> str | None:
        decoded = jwt.decode(value, self.secret, algorithms=["HS256"])
        return decoded.get("id")
