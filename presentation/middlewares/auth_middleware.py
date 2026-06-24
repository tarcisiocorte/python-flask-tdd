from __future__ import annotations

from domain.usecases import LoadAccountByToken
from presentation.controllers._helpers import run_async
from presentation.errors import AccessDeniedError
from presentation.helpers.http_helper import forbidden, ok, server_error
from presentation.protocols import HttpRequest, HttpResponse, Middleware


class AuthMiddleware(Middleware):
    def __init__(self, load_account_by_token: LoadAccountByToken, role: str | None = None):
        self.load_account_by_token = load_account_by_token
        self.role = role

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            headers = {key.lower(): value for key, value in http_request.headers.items()}
            access_token = headers.get("x-access-token")
            if access_token:
                account = run_async(self.load_account_by_token.load(access_token, self.role))
                if account:
                    return ok({"account_id": account.id, "accountId": account.id})
            return forbidden(AccessDeniedError())
        except Exception as error:
            return server_error(error)
