from django.core.paginator import Paginator

from yatube.settings import POSTS_PER_PAGE


def paginator(request, posts: int) -> int:
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page = paginator.get_page(request.GET.get('page'))
    return page
