"""Shared pytest configuration, fixtures, and test utilities."""
from __future__ import annotations

import sys
import uuid
from pathlib import Path
from typing import Any, Dict

import pytest

# Add project root to Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


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

