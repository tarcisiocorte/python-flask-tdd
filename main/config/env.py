import os
import secrets
from functools import lru_cache


def _is_local_context() -> bool:
    environment = (
        os.getenv("ENV")
        or os.getenv("APP_ENV")
        or os.getenv("FLASK_ENV")
        or os.getenv("PYTHON_ENV")
        or "local"
    ).lower()
    return environment in {"local", "test", "testing", "development"}


@lru_cache(maxsize=1)
def jwt_secret() -> str:
    """Return one JWT secret for the lifetime of the application process."""
    configured_secret = os.getenv("JWT_SECRET")
    if configured_secret:
        return configured_secret
    if not _is_local_context():
        raise RuntimeError("JWT_SECRET is required outside local and test environments")
    return secrets.token_urlsafe(32)
