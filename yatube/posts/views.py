from typing import Any

from core.utils import paginator

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from posts.forms import CommentForm, PostForm
from posts.models import Follow, Group, Post

User = get_user_model()


@cache_page(20, key_prefix='index_page')
def index(request: str) -> str:
    return render(
        request,
        'posts/index.html',
        {
            'posts': Post.objects.select_related('author', 'group'),
            'page_obj': paginator(
                request,
                Post.objects.select_related('author', 'group'),
            ),
        },
    )


def group_posts(request: str, slug: str) -> str:
    return render(
        request,
        'posts/group_list.html',
        {
            'group': get_object_or_404(Group, slug=slug),
            'page_obj': paginator(
                request,
                get_object_or_404(Group, slug=slug).posts.select_related(
                    'group',
                ),
            ),
        },
    )


def profile(request: str, username: str) -> str:
    return render(
        request,
        'posts/profile.html',
        {
            'author': get_object_or_404(User, username=username),
            'page_obj': paginator(
                request,
                get_object_or_404(
                    User,
                    username=username,
                ).posts.select_related('author'),
            ),
        },
    )


def post_detail(request: Any, pk: int) -> str:
    return render(
        request,
        'posts/post_detail.html',
        {
            'post': get_object_or_404(Post, id=pk),
            'form': CommentForm(request.POST or None),
            'comments': get_object_or_404(Post, id=pk).comments.all(),
        },
    )


@login_required
def post_create(request: Any) -> str:
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form})
    form.instance.author = request.user
    form.save()
    return redirect('posts:profile', request.user)


@login_required
def post_edit(request: Any, pk: int) -> str:
    post = get_object_or_404(Post, id=pk)
    if post.author != request.user:
        return redirect('posts:post_detail', pk=pk)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', pk=pk)
    return render(
        request,
        'posts/create_post.html',
        {'post': post, 'form': form, 'is_edit': True},
    )


@login_required
def add_comment(request: Any, pk: int) -> str:
    post = get_object_or_404(Post, id=pk)
    form = CommentForm(request.POST or None)
    comments = post.comments.all()
    if not form.is_valid():
        return render(
            request,
            'posts/post_detail.html',
            {'post': post, 'form': form, 'comments': comments},
        )
    comment = form.save(commit=False)
    comment.author = request.user
    comment.post = post
    comment.save()
    return redirect('posts:post_detail', pk=pk)


@login_required
def follow_index(request):
    return render(
        request,
        'posts/follow.html',
        {
            'page_obj': paginator(
                request,
                Post.objects.filter(author__following__user=request.user),
            ),
        },
    )


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', author)


@login_required
def profile_unfollow(request, username: str):
    follow = get_object_or_404(
        Follow,
        user=request.user,
        author__username=username,
    )
    follow.delete()
    return redirect('posts:profile', username)
