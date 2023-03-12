from typing import Any

from django.conf import settings
from django.core.paginator import Paginator


def paginator(request: Any, posts: int) -> int:
    return Paginator(posts, settings.TEXTS_PER_PAGE).get_page(
        request.GET.get('page'),
    )
