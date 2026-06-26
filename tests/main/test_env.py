import pytest

from main.config.env import jwt_secret


@pytest.fixture(autouse=True)
def clear_jwt_secret_cache():
    jwt_secret.cache_clear()
    yield
    jwt_secret.cache_clear()


def test_reuses_generated_jwt_secret_within_process(monkeypatch):
    monkeypatch.delenv("JWT_SECRET", raising=False)
    monkeypatch.setenv("ENV", "test")

    first_secret = jwt_secret()
    second_secret = jwt_secret()

    assert first_secret
    assert first_secret == second_secret


def test_uses_configured_jwt_secret(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "configured-secret")
    monkeypatch.setenv("ENV", "production")

    assert jwt_secret() == "configured-secret"


def test_requires_jwt_secret_outside_local_contexts(monkeypatch):
    monkeypatch.delenv("JWT_SECRET", raising=False)
    monkeypatch.setenv("ENV", "production")

    with pytest.raises(RuntimeError, match="JWT_SECRET is required"):
        jwt_secret()
