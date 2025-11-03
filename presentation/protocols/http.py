from typing import Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class HttpResponse:
    status_code: int
    body: Any


class HttpRequest:
    def __init__(self, body: Optional[Dict[str, Any]] = None):
        self.body = body or {}

