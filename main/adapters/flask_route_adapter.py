from dataclasses import asdict, is_dataclass
from typing import Any

from flask import jsonify, request

from presentation.protocols import Controller, HttpRequest


def _serialize(value: Any) -> Any:
    if isinstance(value, Exception):
        return str(value)
    if is_dataclass(value):
        return {key: _serialize(item) for key, item in asdict(value).items()}
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    return value


def adapt_route(controller: Controller):
    def route(**params):
        http_request = HttpRequest(
            body=request.get_json(silent=True) or {},
            params=params,
            account_id=getattr(request, "account_id", None),
        )
        http_response = controller.handle(http_request)
        if 200 <= http_response.status_code <= 299:
            body = _serialize(http_response.body)
            if http_response.status_code == 204:
                return ("", 204)
            return jsonify(body), http_response.status_code
        return jsonify({"error": str(http_response.body)}), http_response.status_code

    return route
