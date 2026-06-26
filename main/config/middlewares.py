from __future__ import annotations

import os
import time

from flask import Flask, Response, request


_NO_CACHE = "no-store, no-cache, must-revalidate, proxy-revalidate"
_DEFAULT_CORS_ORIGINS = "http://localhost:3000"
_DEFAULT_CORS_METHODS = "GET,POST,PUT,DELETE,OPTIONS"
_DEFAULT_CORS_HEADERS = "Content-Type,Authorization,x-access-token"
_AUTH_PATHS = {"/api/login", "/api/signup", "/signup"}


def _csv_env(name: str, default: str) -> list[str]:
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]


def setup_middlewares(app: Flask) -> None:
    auth_attempts: dict[tuple[str, str], list[float]] = {}

    @app.before_request
    def handle_preflight() -> Response | None:
        if request.method == "OPTIONS":
            return app.response_class(status=204)
        if request.path in _AUTH_PATHS:
            max_requests = int(os.getenv("AUTH_RATE_LIMIT_MAX_REQUESTS", "5"))
            window_seconds = int(os.getenv("AUTH_RATE_LIMIT_WINDOW_SECONDS", "60"))
            now = time.monotonic()
            key = (request.path, request.remote_addr or "unknown")
            attempts = [
                attempted_at
                for attempted_at in auth_attempts.get(key, [])
                if now - attempted_at < window_seconds
            ]
            if len(attempts) >= max_requests:
                response = app.json.response({"error": "Too many requests"})
                response.status_code = 429
                response.headers["Retry-After"] = str(window_seconds)
                auth_attempts[key] = attempts
                return response
            attempts.append(now)
            auth_attempts[key] = attempts
        return None

    @app.after_request
    def add_response_headers(response: Response) -> Response:
        if response.status_code != 204 and response.is_json:
            response.headers["Content-Type"] = "application/json"

        allowed_origins = _csv_env("CORS_ALLOWED_ORIGINS", _DEFAULT_CORS_ORIGINS)
        request_origin = request.headers.get("Origin")
        allowed_origin = (
            request_origin
            if request_origin in allowed_origins
            else allowed_origins[0]
        )

        response.headers["Access-Control-Allow-Origin"] = allowed_origin
        response.headers["Vary"] = "Origin"
        response.headers["Access-Control-Allow-Methods"] = ",".join(
            _csv_env("CORS_ALLOWED_METHODS", _DEFAULT_CORS_METHODS)
        )
        response.headers["Access-Control-Allow-Headers"] = ",".join(
            _csv_env("CORS_ALLOWED_HEADERS", _DEFAULT_CORS_HEADERS)
        )
        response.headers["Cache-Control"] = _NO_CACHE
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers["Surrogate-Control"] = "no-store"
        return response
