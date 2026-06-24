# AGENTS.md - Modern Flask Project

## Project Overview

A modern Python Flask web API following Clean Architecture principles with TDD, using UV for packaging, Ruff for code quality, and pytest for testing.

**Tech Stack:**
Python 3.12+
Flask 3.x
Flask-RESTX for REST API resources and OpenAPI documentation
UV for dependency management, virtual environments, locking, and command execution
Ruff for linting and formatting
pytest for unit and integration tests
pytest-cov for coverage reporting
pytest-asyncio when async boundaries need to be tested
SQLAlchemy 2.x using typed declarative mappings
Alembic for database migrations
Pydantic v2 for request/response validation and DTOs

**Python Style Guidelines**

Use modern Python 3.12+ features where they improve clarity:

Prefer pathlib.Path over string path manipulation.
Prefer typing.Protocol for application ports.
Prefer dataclasses.dataclass(frozen=True, slots=True) for simple immutable domain models.
Prefer Pydantic v2 models for API input/output schemas.
Prefer explicit return types on public functions.
Prefer match only when it makes branching clearer.
Use StrEnum for string-based enumerations.
Avoid global mutable state.
Avoid service locators outside the composition root.
Avoid framework imports in domain and application layers.

Example:

from dataclasses import dataclass
from enum import StrEnum


class Environment(StrEnum):
    LOCAL = "local"
    TEST = "test"
    PRODUCTION = "production"


@dataclass(frozen=True, slots=True)
class HealthStatus:
    status: str


**Tasks details:**
See the document FEATURE_PARITY_PLAN.md
Also see the project in the /Users/tarcisiocorte/dev/clean-ts-api

Please, implement the all the code for the Phase 3: Middleware Parity

Implement Python equivalents for TypeScript middlewares.

1. `body_parser`
   - Mostly already covered by Flask.
   - Keep tests verifying JSON parsing.

2. `content_type`
   - Add `Content-Type: application/json` on JSON responses.
   - Avoid breaking empty `204` responses.

3. `cors`
   - Add headers:
     - `Access-Control-Allow-Origin: *`
     - `Access-Control-Allow-Methods`
     - `Access-Control-Allow-Headers`
   - Handle `OPTIONS` preflight.

4. `no_cache`
   - Add:
     - `Cache-Control: no-store, no-cache, must-revalidate, proxy-revalidate`
     - `Pragma: no-cache`
     - `Expires: 0`

5. `auth`
   - Use existing `presentation/middlewares/auth_middleware.py`.
   - Adapt it through `main/adapters/flask_middleware_adapter.py`.

6. `admin_auth`
   - Use the same middleware, but with role `"admin"`.

7. Route middleware wiring:
   - `POST /api/surveys`: admin auth.
   - `GET /api/surveys`: user auth.
   - Survey result routes: user auth.

Deliverable: route-level anonymous, user, and admin behavior matches the TypeScript project.