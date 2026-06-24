from functools import wraps

from flask import jsonify, request

from presentation.protocols import HttpRequest, Middleware


def adapt_middleware(middleware: Middleware):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            headers = {key.lower(): value for key, value in request.headers.items()}
            http_request = HttpRequest(
                headers=headers,
            )
            http_response = middleware.handle(http_request)
            if http_response.status_code == 200:
                for key, value in http_response.body.items():
                    setattr(request, key, value)
                return view(*args, **kwargs)
            error = getattr(http_response.body, "message", str(http_response.body))
            return jsonify({"error": error}), http_response.status_code

        return wrapped

    return decorator
