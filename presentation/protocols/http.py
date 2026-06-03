from typing import Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class HttpResponse:
    status_code: int
    body: Any


class HttpRequest:
    def __init__(
        self,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        account_id: Optional[str] = None,
    ):
        self.body = body or {}
        self.headers = headers or {}
        self.params = params or {}
        self.account_id = account_id
