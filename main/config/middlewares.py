from __future__ import annotations

from flask import Flask, Response, request


_NO_CACHE = "no-store, no-cache, must-revalidate, proxy-revalidate"


def setup_middlewares(app: Flask) -> None:
    @app.before_request
    def handle_preflight() -> Response | None:
        if request.method == "OPTIONS":
            return app.response_class(status=204)
        return None

    @app.after_request
    def add_response_headers(response: Response) -> Response:
        if response.status_code != 204 and response.is_json:
            response.headers["Content-Type"] = "application/json"

        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Cache-Control"] = _NO_CACHE
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers["Surrogate-Control"] = "no-store"
        return response
