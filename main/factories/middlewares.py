from __future__ import annotations

import os

from data.usecases import DbLoadAccountByToken
from infra.cryptography import JwtAdapter
from infra.db.mongodb import AccountMongoRepository
from presentation.middlewares import AuthMiddleware


def make_auth_middleware(role: str | None = None):
    return AuthMiddleware(
        DbLoadAccountByToken(
            JwtAdapter(os.getenv("JWT_SECRET", "secret")),
            AccountMongoRepository(),
        ),
        role,
    )
