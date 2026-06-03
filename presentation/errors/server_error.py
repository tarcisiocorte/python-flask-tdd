from __future__ import annotations

class ServerError(Exception):
    def __init__(self, error: Exception | None = None):
        self.stack = str(error) if error else None
        super().__init__(self.stack or "Internal server error")
