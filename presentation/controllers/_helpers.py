from __future__ import annotations

import asyncio
from typing import Any

from presentation.protocols.http import HttpRequest


def request_data(request: HttpRequest | dict[str, Any]) -> dict[str, Any]:
    if isinstance(request, HttpRequest):
        return {
            **request.body,
            **request.params,
            "account_id": request.account_id,
            "accountId": request.account_id,
        }
    return request


def run_async(coro: Any) -> Any:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    raise RuntimeError("Cannot synchronously run async controller inside a running event loop")
