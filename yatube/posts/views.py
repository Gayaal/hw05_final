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
    posts = Post.objects.select_related('author', 'group')
    page = paginator(request, posts)
    return render(
        request,
        'posts/index.html',
        {
            'posts': posts,
            'page_obj': page,
        },
    )


def group_posts(request: str, slug: str) -> str:
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('group')
    page = paginator(request, posts)
    return render(
        request,
        'posts/group_list.html',
        {
            'group': group,
            'posts': posts,
            'page_obj': page,
        },
    )


def profile(request: str, username: str) -> str:
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('author')
    page = paginator(request, posts)
    return render(
        request,
        'posts/profile.html',
        {
            'author': author,
            'page_obj': page,
        },
    )


def post_detail(request: str, pk: int) -> str:
    post = get_object_or_404(Post, id=pk)
    form = CommentForm(request.POST or None)
    comments = post.comments.all()
    return render(
        request,
        'posts/post_detail.html',
        {
            'post': post,
            'form': form,
            'comments': comments,
        },
    )


@login_required
def post_create(request: str) -> str:
    form = PostForm(request.POST or None)
    if form.is_valid():
        temp_form = form.save(commit=False)
        temp_form.author = request.user
        temp_form.save()
        return redirect('posts:profile', temp_form.author)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request: str, pk: int) -> str:
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
def add_comment(request: str, pk: int) -> str:
    post = get_object_or_404(Post, id=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('posts:post_detail', pk=pk)
    comments = post.comments.all()
    return render(
        request,
        'posts/post_detail.html',
        {'post': post, 'form': form, 'comments': comments},
    )


@login_required
def follow_index(request: str) -> str:
    post_list = Post.objects.filter(author__following__user=request.user)
    page_obj = paginator(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request: str, username: str) -> str:
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request: str, username: str) -> str:
    author = get_object_or_404(User, username=username)
    request.user.follower.filter(author=author).delete()
    return redirect('posts:profile', username)
