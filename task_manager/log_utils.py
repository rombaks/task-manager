import logging
from threading import local
from typing import Any, Callable

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)
_thread_locals = local()


class LoggingMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        _thread_locals.request = request
        response = self.get_response(request)
        return response

    def process_view(self, request: HttpRequest, view_func: Callable, *_: Any) -> None:
        _thread_locals.view = view_func


class RequestFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        request = _thread_locals.request
        record.request = request
        record.view = _thread_locals.view
        record.user_id = request.user.id if request.user.is_authenticated else "-"
        return super().format(record)


class PlaceHolder:
    def __init__(self, to_str: str = "-") -> None:
        self._to_str = to_str

    def __getattr__(self, name: str) -> "PlaceHolder":
        return self

    def __call__(self, *args: Any, **kwargs: Any) -> "PlaceHolder":
        return self

    def __str__(self) -> str:
        return self._to_str

    def __repr__(self) -> str:
        return self._to_str

    def __bool__(self) -> bool:
        return False
