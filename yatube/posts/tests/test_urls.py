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
        cls.anonymous = Client()
        cls.urls = {
            'group_list': reverse('posts:group_list', args=(cls.group.slug,)),
            'profile': reverse('posts:profile', args=(cls.author,)),
            'post_edit': reverse('posts:post_edit', args=(cls.post.pk,)),
            'add_comment': reverse('posts:add_comment', args=(cls.post.pk,)),
            'post_detail': reverse('posts:post_detail', args=(cls.post.pk,)),
            'post_create': reverse('posts:post_create'),
            'follow_index': reverse('posts:follow_index'),
            'profile_follow': reverse(
                'posts:profile_follow',
                args=(cls.author,),
            ),
            'profile_unfollow': reverse(
                'posts:profile_unfollow',
                args=(cls.author,),
            ),
            'index': reverse('posts:index'),
        }

    def test_http_statuses(self) -> None:
        httpstatuses = (
            (self.urls['group_list'], HTTPStatus.OK, self.anonymous),
            (self.urls['profile'], HTTPStatus.OK, self.anonymous),
            (self.urls['post_edit'], HTTPStatus.FOUND, self.anonymous),
            (self.urls['post_edit'], HTTPStatus.FOUND, self.authorized_client),
            (self.urls['post_edit'], HTTPStatus.OK, self.author_client),
            (self.urls['add_comment'], HTTPStatus.FOUND, self.anonymous),
            (self.urls['add_comment'], HTTPStatus.OK, self.authorized_client),
            (self.urls['add_comment'], HTTPStatus.OK, self.author_client),
            (self.urls['post_detail'], HTTPStatus.OK, self.anonymous),
            (self.urls['post_create'], HTTPStatus.FOUND, self.anonymous),
            (self.urls['post_create'], HTTPStatus.OK, self.authorized_client),
            (self.urls['follow_index'], HTTPStatus.OK, self.author_client),
            (
                self.urls['profile_follow'],
                HTTPStatus.FOUND,
                self.anonymous,
            ),
            (
                self.urls['profile_follow'],
                HTTPStatus.FOUND,
                self.authorized_client,
            ),
            (
                self.urls['profile_follow'],
                HTTPStatus.FOUND,
                self.author_client,
            ),
            (
                self.urls['profile_unfollow'],
                HTTPStatus.FOUND,
                self.anonymous,
            ),
            (
                self.urls['profile_unfollow'],
                HTTPStatus.FOUND,
                self.authorized_client,
            ),
            (
                self.urls['profile_unfollow'],
                HTTPStatus.NOT_FOUND,
                self.author_client,
            ),
            (self.urls['index'], HTTPStatus.OK, self.anonymous),
        )
        for url, response_code, test_client in httpstatuses:
            with self.subTest(url=url):
                self.assertEqual(
                    test_client.get(url).status_code,
                    response_code,
                )

    def test_redirects(self) -> None:
        redirects = (
            (
                self.urls['post_create'],
                reverse('login') + '?next=' + reverse('posts:post_create'),
                self.anonymous,
            ),
            (
                self.urls['post_create'],
                reverse('login') + '?next=' + reverse('posts:post_create'),
                self.anonymous,
            ),
            (
                self.urls['post_edit'],
                reverse('login')
                + '?next='
                + reverse('posts:post_edit', args=(self.post.pk,)),
                self.anonymous,
            ),
        )
        for url, redirect, test_client in redirects:
            with self.subTest(url=url):
                self.assertRedirects(test_client.get(url), redirect)

    def test_templates(self) -> None:
        templates = (
            (
                self.urls['group_list'],
                'posts/group_list.html',
                self.anonymous,
            ),
            (
                self.urls['profile'],
                'posts/profile.html',
                self.anonymous,
            ),
            (
                self.urls['post_edit'],
                'posts/create_post.html',
                self.authorized_client,
            ),
            (
                self.urls['post_detail'],
                'posts/post_detail.html',
                self.anonymous,
            ),
            (
                self.urls['post_create'],
                'posts/create_post.html',
                self.authorized_client,
            ),
            (
                self.urls['index'],
                'posts/index.html',
                self.anonymous,
            ),
        )
        for url, template, test_client in templates:
            with self.subTest(url=url):
                self.assertTemplateUsed(test_client.get(url), template)

        # qwerty = reverse('posts:index')
        # response = self.authorized_client.get(qwerty)
        # templates_name = [qwerty.name for qwerty in response.templates]
        # print('здесь должны быть названия шаблонов!')
        # print(templates_name)
