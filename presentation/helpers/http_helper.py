from typing import Optional

from presentation.protocols.http import HttpResponse
from presentation.errors.server_error import ServerError


def bad_request(error: Exception) -> HttpResponse:
    return HttpResponse(
        status_code=400,
        body=error
    )


def server_error(error: Optional[Exception] = None) -> HttpResponse:
    return HttpResponse(
        status_code=500,
        body=ServerError(error)
    )


def ok(data: any) -> HttpResponse:
    return HttpResponse(
        status_code=200,
        body=data
    )


def forbidden(error: Exception) -> HttpResponse:
    return HttpResponse(status_code=403, body=error)


def unauthorized(error: Optional[Exception] = None) -> HttpResponse:
    from presentation.errors import UnauthorizedError

    error = error or UnauthorizedError()
    return HttpResponse(status_code=401, body=error)


def no_content() -> HttpResponse:
    return HttpResponse(status_code=204, body=None)
