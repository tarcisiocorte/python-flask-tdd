from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import jwt
from jwt import InvalidTokenError

from data.protocols.encrypter import Decrypter, Encrypter


class JwtAdapter(Encrypter, Decrypter):
    def __init__(
        self,
        secret: str,
        expires_in_seconds: int | None = None,
        issuer: str | None = None,
        audience: str | None = None,
    ):
        self.secret = secret
        self.expires_in_seconds = expires_in_seconds or int(
            os.getenv("JWT_EXPIRES_IN_SECONDS", "3600")
        )
        self.issuer = issuer or os.getenv("JWT_ISSUER", "python-flask-tdd")
        self.audience = audience or os.getenv("JWT_AUDIENCE", "python-flask-tdd-api")

    async def encrypt(self, value: str) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "id": value,
            "iat": now,
            "exp": now + timedelta(seconds=self.expires_in_seconds),
            "iss": self.issuer,
            "aud": self.audience,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    async def decrypt(self, value: str) -> str | None:
        try:
            decoded = jwt.decode(
                value,
                self.secret,
                algorithms=["HS256"],
                issuer=self.issuer,
                audience=self.audience,
                options={"require": ["exp", "iat", "iss", "aud"]},
            )
        except InvalidTokenError:
            return None
        return decoded.get("id")
