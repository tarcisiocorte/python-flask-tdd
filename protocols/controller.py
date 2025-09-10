from abc import ABC, abstractmethod
from protocols.http import HttpRequest, HttpResponse


class Controller(ABC):
    @abstractmethod
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        pass
