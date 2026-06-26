import asyncio
from datetime import datetime, timedelta, timezone

import jwt

from infra.cryptography.jwt_adapter import JwtAdapter


def test_jwt_adapter_adds_required_claims_and_decrypts_token():
    sut = JwtAdapter(
        "secret",
        expires_in_seconds=60,
        issuer="issuer",
        audience="audience",
    )

    token = asyncio.run(sut.encrypt("account_id"))
    decoded = jwt.decode(
        token,
        "secret",
        algorithms=["HS256"],
        issuer="issuer",
        audience="audience",
    )

    assert decoded["id"] == "account_id"
    assert decoded["iss"] == "issuer"
    assert decoded["aud"] == "audience"
    assert "iat" in decoded
    assert "exp" in decoded
    assert asyncio.run(sut.decrypt(token)) == "account_id"


def test_jwt_adapter_rejects_tokens_without_required_claims():
    sut = JwtAdapter("secret", issuer="issuer", audience="audience")
    token = jwt.encode({"id": "account_id"}, "secret", algorithm="HS256")

    assert asyncio.run(sut.decrypt(token)) is None


def test_jwt_adapter_rejects_expired_tokens():
    sut = JwtAdapter("secret", issuer="issuer", audience="audience")
    now = datetime.now(timezone.utc)
    token = jwt.encode(
        {
            "id": "account_id",
            "iat": now - timedelta(minutes=10),
            "exp": now - timedelta(minutes=1),
            "iss": "issuer",
            "aud": "audience",
        },
        "secret",
        algorithm="HS256",
    )

    assert asyncio.run(sut.decrypt(token)) is None
