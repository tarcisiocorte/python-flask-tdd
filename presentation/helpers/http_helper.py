from protocols.http import HttpResponse
from errors.server_error import ServerError


def bad_request(error: Exception) -> HttpResponse:
    return HttpResponse(
        status_code=400,
        body=error
    )


def server_error() -> HttpResponse:
    return HttpResponse(
        status_code=500,
        body=ServerError()
    )


def ok(data: any) -> HttpResponse:
    return HttpResponse(
        status_code=200,
        body=data
    )
