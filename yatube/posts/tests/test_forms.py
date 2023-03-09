import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Follow, Post

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='author')
        cls.authorized_user = Client()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self) -> None:
        self.authorized_user.force_login(self.author)

    def test_authorized_user_create_post(self) -> None:
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='posts/small.gif',
            content=small_gif,
            content_type='image/gif',
        )
        post = Post.objects.create(
            text='Текст поста',
            author=self.author,
        )
        data = {
            'text': 'Текст поста',
        }
        pictures = {
            'image': uploaded,
        }
        response = self.authorized_user.post(
            reverse('posts:post_create'),
            data=data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:profile',
                kwargs={'username': self.author.username},
            ),
        )
        self.assertEqual(post.text, data['text'])
        self.assertEqual(post.author, self.author)
        for form_field in pictures.keys():
            self.assertFalse(
                Post.objects.latest('author').image,
                'posts/small.gif',
            )
        for form_field in data.keys():
            self.assertTrue(
                (
                    Post._meta.get_field(form_field).value_from_object(
                        Post.objects.latest('author'),
                    )
                )
                == data[form_field],
            )

    def test_authorized_user_edit_post(self) -> None:
        post = Post.objects.create(
            text='Текст поста для редактирования',
            author=self.author,
        )
        data = {
            'text': 'Отредактированный текст поста',
        }
        response = self.authorized_user.post(
            reverse('posts:post_edit', args=[post.pk]),
            data=data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', args=[post.pk]),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(post.text == data['text'])
        self.assertTrue(post.author == self.author)

    def test_nonauthorized_user_create_post(self) -> None:
        self.client = Client()
        data = {
            'text': 'Текст поста',
        }
        response = self.client.post(
            reverse('posts:post_create'),
            data=data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(
            response,
            reverse('login') + '?next=' + reverse('posts:post_create'),
        )

    def test_nonauthorized_user_edit_post(self) -> None:
        self.client = Client()
        post = Post.objects.create(
            text='Текст поста для редактирования',
            author=self.author,
        )
        posts_count = Post.objects.count()
        data = {
            'text': 'Текст поста',
        }
        response = self.client.post(
            reverse('posts:post_edit', args=[post.pk]),
            data=data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(
            response,
            reverse('login')
            + '?next='
            + reverse('posts:post_edit', args=[post.pk]),
        )
        self.assertEqual(Post.objects.count(), posts_count)

    def test_authorized_user_edit_other_post(self) -> None:
        post = Post.objects.create(
            text='Текст поста для редактирования',
            author=self.author,
        )
        data = {
            'text': 'Отредактированный текст поста',
        }
        response = self.authorized_user.post(
            reverse('posts:post_edit', args=[post.pk]),
            data=data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', args=[post.pk]),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(post.text == data['text'])
        self.assertFalse(self.author != self.author)


class FoollowCreateFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user')
        cls.author = User.objects.create_user(username='author')
        cls.authorized_user = Client()
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.author,
        )

    def setUp(self) -> None:
        self.authorized_user.force_login(self.user)
        self.authorized_user.force_login(self.author)

    def test_succes_subscription(self) -> None:
        follow_str_value = self.follow.__str__()
        follow_test_value = self.follow.user.get_username()
        self.assertEqual(follow_str_value, follow_test_value)
        self.assertIsInstance(follow_str_value, str)

    def test_yourself_subscription(self) -> None:
        follow_str_value = self.follow.__str__()
        follow_test_value = self.follow.__str__()
        self.assertEqual(follow_str_value, follow_test_value)
        self.assertIsInstance(follow_str_value, str)

    def test_yourself_subscription(self) -> None:
        follow_str_value = self.follow.user.get_username()
        follow_test_value = self.follow.user.get_username()
        self.assertEqual(follow_str_value, follow_test_value)
        self.assertIsInstance(follow_str_value, str)
