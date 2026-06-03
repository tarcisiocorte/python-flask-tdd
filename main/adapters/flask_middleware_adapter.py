from functools import wraps

from flask import jsonify, request

from presentation.protocols import HttpRequest, Middleware


def adapt_middleware(middleware: Middleware):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            http_request = HttpRequest(
                headers=dict(request.headers),
                body={
                    "access_token": request.headers.get("x-access-token"),
                    "accessToken": request.headers.get("x-access-token"),
                },
            )
            http_response = middleware.handle(http_request)
            if http_response.status_code == 200:
                for key, value in http_response.body.items():
                    setattr(request, key, value)
                return view(*args, **kwargs)
            return jsonify({"error": str(http_response.body)}), http_response.status_code

        return wrapped

    return decorator
