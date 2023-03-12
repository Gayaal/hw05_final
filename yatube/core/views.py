from http import HTTPStatus
from typing import Any

from django.shortcuts import render


def page_not_found(request: Any, exception: str) -> str:
    del exception
    return render(
        request,
        'core/404.html',
        {'path': request.path},
        status=HTTPStatus.NOT_FOUND,
    )


def server_error(request: str) -> str:
    return render(
        request,
        'core/500.html',
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )


def csrf_failure(request: str, reason: str = '') -> str:
    del reason
    return render(
        request,
        'core/403csrf.html',
        status=HTTPStatus.FORBIDDEN,
    )
