from main.config.env import jwt_secret


def test_reuses_generated_jwt_secret_within_process(monkeypatch):
    monkeypatch.delenv("JWT_SECRET", raising=False)
    jwt_secret.cache_clear()

    first_secret = jwt_secret()
    second_secret = jwt_secret()

    assert first_secret == second_secret
