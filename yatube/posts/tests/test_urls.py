from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.auth = User.objects.create_user(username='HasNoName')
        cls.author = User.objects.create_user(username='Author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый текст',
        )
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.auth)
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.urls = {
            'index': reverse('posts:index'),
            'post_create': reverse('posts:post_create'),
            'group_list': reverse('posts:group_list', args=(cls.group.slug,)),
            'post_detail': reverse('posts:post_detail', args=(cls.post.pk,)),
            'post_edit': reverse('posts:post_edit', args=(cls.post.pk,)),
            'profile': reverse('posts:profile', args=(cls.author,)),
        }

    def test_http_statuses(self) -> None:
        httpstatuses = (
            (self.urls['index'], HTTPStatus.OK, self.authorized_client),
            (self.urls['post_create'], HTTPStatus.OK, self.author_client),
            (
                self.urls['post_create'],
                HTTPStatus.OK,
                self.authorized_client,
            ),
            (self.urls['group_list'], HTTPStatus.OK, self.authorized_client),
            (self.urls['post_detail'], HTTPStatus.OK, self.authorized_client),
            (self.urls['post_edit'], HTTPStatus.OK, self.author_client),
            (self.urls['profile'], HTTPStatus.OK, self.authorized_client),
        )
        for url, response_code, test_client in httpstatuses:
            with self.subTest(url=url):
                self.assertEqual(
                    test_client.get(url).status_code,
                    response_code,
                )


'''

    def test_templates(self) -> None:
        templates = (
            (self.urls['index'], 'posts/index.html', self.authorized_client),
            (
                self.urls['post_create'],
                'posts/create_post.html',
                self.author_client,
            ),
            (
                self.urls['post_create'],
                'posts/create_post.html',
                self.authorized_client,
            ),
            (
                self.urls['group_list'],
                'posts/group_list.html',
                self.authorized_client,
            ),
            (
                self.urls['post_detail'],
                'posts/post_detail.html',
                self.authorized_client,
            ),
            (
                self.urls['post_edit'],
                'posts/create_post.html',
                self.author_client,
            ),
            (
                self.urls['profile'],
                'posts/profile.html',
                self.authorized_client,
            ),
        )
        for url, template, test_client in templates:
            with self.subTest(url=url):
                self.assertTemplateUsed(test_client.get(url), template)


    def test_redirects(self) -> None:
        redirects = (
            (
                self.urls['post_create'],
                '/posts/{self.post.pk}/',
                self.author_client,
            ),
            (
                self.urls['post_create'],
                '/posts/{self.post.pk}/',
                self.authorized_client,
            ),
            (
                self.urls['post_edit'],
                '/posts/{self.post.pk}/edit/',
                self.author_client,
            ),
        )
        for url, redirect, test_client in redirects:
            with self.subTest(url=url):
                self.assertRedirects(test_client.get(url), redirect)
'''
