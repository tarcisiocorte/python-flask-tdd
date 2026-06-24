from __future__ import annotations

from data.usecases import DbLoadAccountByToken
from infra.cryptography import JwtAdapter
from infra.db.mongodb import AccountMongoRepository
from main.config.env import jwt_secret
from presentation.middlewares import AuthMiddleware


def make_auth_middleware(role: str | None = None):
    return AuthMiddleware(
        DbLoadAccountByToken(
            JwtAdapter(jwt_secret()),
            AccountMongoRepository(),
        ),
        role,
    )
