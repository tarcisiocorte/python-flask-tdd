import pytest

from main.config.env import jwt_secret


def test_reuses_generated_jwt_secret_within_process(monkeypatch):
    monkeypatch.delenv("JWT_SECRET", raising=False)
    monkeypatch.setenv("ENV", "test")
    jwt_secret.cache_clear()

    first_secret = jwt_secret()
    second_secret = jwt_secret()

    assert first_secret == second_secret


def test_uses_configured_jwt_secret(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "configured-secret")
    monkeypatch.setenv("ENV", "production")
    jwt_secret.cache_clear()

    assert jwt_secret() == "configured-secret"


def test_requires_jwt_secret_outside_local_contexts(monkeypatch):
    monkeypatch.delenv("JWT_SECRET", raising=False)
    monkeypatch.setenv("ENV", "production")
    jwt_secret.cache_clear()

    with pytest.raises(RuntimeError, match="JWT_SECRET is required"):
        jwt_secret()
