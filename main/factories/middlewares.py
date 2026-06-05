from __future__ import annotations

import os
import secrets

from data.usecases import DbLoadAccountByToken
from infra.cryptography import JwtAdapter
from infra.db.mongodb import AccountMongoRepository
from presentation.middlewares import AuthMiddleware


def _jwt_secret() -> str:
    return os.getenv("JWT_SECRET") or secrets.token_urlsafe(32)


def make_auth_middleware(role: str | None = None):
    return AuthMiddleware(
        DbLoadAccountByToken(
            JwtAdapter(_jwt_secret()),
            AccountMongoRepository(),
        ),
        role,
    )
