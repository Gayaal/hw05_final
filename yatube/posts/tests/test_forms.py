import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Post

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post_author = User.objects.create_user(username='post_author')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self) -> None:
        self.client = Client()

    def test_authorized_user_create_post(self) -> None:
        self.authorized_user = Client()
        self.authorized_user.force_login(self.post_author)
        post = Post.objects.create(
            text='Текст поста',
            author=self.post_author,
        )
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
        data = {
            'text': 'Текст поста',
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
                kwargs={'username': self.post_author.username},
            ),
        )
        self.assertEqual(post.text, data['text'])
        self.assertEqual(post.author, self.post_author)
        for form_field in data.keys():
            if form_field == 'image':
                self.assertFalse(
                    Post.objects.latest('author').image,
                    'posts/small.gif',
                )
            else:
                self.assertTrue(
                    (
                        Post._meta.get_field(form_field).value_from_object(
                            Post.objects.latest('author')
                        )
                    )
                    == data[form_field]
                )

    def test_authorized_user_edit_post(self) -> None:
        self.authorized_user = Client()
        self.authorized_user.force_login(self.post_author)
        post = Post.objects.create(
            text='Текст поста для редактирования',
            author=self.post_author,
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
            response, reverse('posts:post_detail', args=[post.pk])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(post.text == data['text'])
        self.assertTrue(post.author == self.post_author)

    def test_nonauthorized_user_create_post(self) -> None:
        posts_count = Post.objects.count()
        data = {
            'text': 'Текст поста',
        }
        response = self.client.post(
            reverse('posts:post_create'), data=data, follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(
            response,
            reverse('login') + '?next=' + reverse('posts:post_create'),
        )
        self.assertEqual(Post.objects.count(), posts_count)

    def test_nonauthorized_user_edit_post(self) -> None:
        posts_count = Post.objects.count()
        post = Post.objects.create(
            text='Текст поста для редактирования',
            author=self.post_author,
        )
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
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_authorized_user_edit_other_post(self) -> None:
        self.authorized_user = Client()
        self.authorized_user.force_login(self.post_author)
        post = Post.objects.create(
            text='Текст поста для редактирования',
            author=self.post_author,
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
            response, reverse('posts:post_detail', args=[post.pk])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(post.text == data['text'])
        self.assertFalse(self.post_author != self.post_author)
