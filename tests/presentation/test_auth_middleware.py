from dataclasses import dataclass
from unittest.mock import AsyncMock

from presentation.middlewares import AuthMiddleware
from presentation.protocols import HttpRequest


@dataclass
class Account:
    id: str


def test_reads_access_token_from_headers_and_forwards_role():
    load_account_by_token = AsyncMock()
    load_account_by_token.load.return_value = Account("account-123")
    middleware = AuthMiddleware(load_account_by_token, "admin")

    response = middleware.handle(
        HttpRequest(headers={"X-Access-Token": "valid-token"})
    )

    assert response.status_code == 200
    assert response.body == {
        "account_id": "account-123",
        "accountId": "account-123",
    }
    load_account_by_token.load.assert_awaited_once_with("valid-token", "admin")


def test_rejects_missing_access_token():
    load_account_by_token = AsyncMock()
    middleware = AuthMiddleware(load_account_by_token)

    response = middleware.handle(HttpRequest())

    assert response.status_code == 403
    assert str(response.body) == "Access denied"
    load_account_by_token.load.assert_not_awaited()
