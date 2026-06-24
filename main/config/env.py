import os
import secrets
from functools import lru_cache


@lru_cache(maxsize=1)
def jwt_secret() -> str:
    """Return one JWT secret for the lifetime of the application process."""
    return os.getenv("JWT_SECRET") or secrets.token_urlsafe(32)
