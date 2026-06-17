"""Shared pytest configuration, fixtures, and test utilities."""
from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path
from typing import Any, Dict
from urllib.parse import quote_plus

import pytest

# Add project root to Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def _load_dotenv() -> None:
    env_path = project_root / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _configure_default_mongo_url() -> None:
    if os.getenv("MONGO_URL") or not os.getenv("MONGO_PASSWORD"):
        return

    user = quote_plus(os.getenv("MONGO_USER", "flask_user"))
    password = quote_plus(os.environ["MONGO_PASSWORD"])
    port = os.getenv("MONGO_PORT", "27017")
    os.environ["MONGO_URL"] = (
        f"mongodb://{user}:{password}@localhost:{port}/?authSource=admin"
    )


def _configure_default_test_database() -> None:
    os.environ.setdefault("MONGO_DB_NAME", "flask_tdd_test")


_load_dotenv()
_configure_default_mongo_url()
_configure_default_test_database()


@pytest.fixture
def random_email() -> str:
    """Generate a unique email to avoid cross-test collisions."""
    return f"test-{uuid.uuid4().hex[:8]}@example.com"


@pytest.fixture
def signup_payload(random_email: str) -> Dict[str, str]:
    """Provide a valid signup payload shared by controller/integration tests."""
    return {
        "name": "Test User",
        "email": random_email,
        "password": "valid_password_123",
        "passwordConfirmation": "valid_password_123",
    }


@pytest.fixture
def make_signup_payload() -> Any:
    """Factory fixture to create payload overrides per test case."""

    def _factory(**overrides: str) -> Dict[str, str]:
        payload = {
            "name": "Test User",
            "email": f"test-{uuid.uuid4().hex[:8]}@example.com",
            "password": "valid_password_123",
            "passwordConfirmation": "valid_password_123",
        }
        payload.update(overrides)
        return payload

    return _factory
