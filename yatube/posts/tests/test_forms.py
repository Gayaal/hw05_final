import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from mixer.backend.django import mixer

from posts.models import Follow, Post
from posts.tests.common import create_image

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='author')
        cls.authorized_user = Client()
        cls.authorized_user.force_login(cls.author)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_authorized_user_create_post(self) -> None:
        image = create_image()
        data = {
            'text': 'Текст поста',
            'image': image,
        }
        self.authorized_user.post(
            reverse('posts:post_create'),
            data=data,
            follow=True,
        )
        image_file = data['image']
        image_file.seek(0)
        new_post = Post.objects.first()
        self.assertEqual(new_post.author, self.author)
        self.assertEqual(new_post.text, data['text'])
        self.assertEqual(new_post.image.file.read(), image_file.read())

    def test_author_can_edit_post(self) -> None:
        post = mixer.blend('posts.Post', author=self.author)
        image = create_image()
        data = {
            'text': 'Изменённый текст поста',
            'group': mixer.blend('posts.Group').pk,
            'image': image,
        }
        self.authorized_user.post(
            reverse('posts:post_edit', args={post.pk}),
            data=data,
            follow=True,
        )
        post.refresh_from_db()
        image_file = data['image']
        image_file.seek(0)
        self.assertEqual(post.text, data['text'])
        self.assertEqual(post.group.pk, data['group'])
        self.assertEqual(post.image.file.read(), image_file.read())

    def test_nonauthorized_user_create_post(self) -> None:
        self.client = Client()
        image = create_image()
        data = {
            'text': 'Текст поста',
            'image': image,
        }
        self.client.post(
            reverse('posts:post_create'),
            data=data,
            follow=True,
        )
        posts_count = Post.objects.count()
        self.assertEqual(Post.objects.all().count(), posts_count)


class FollowCreateFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_follower = User.objects.create_user(username='follower')
        cls.user_following = User.objects.create_user(username='following')
        cls.client_auth_follower = Client()
        cls.client_auth_following = Client()

    def setUp(self) -> None:
        self.client_auth_follower.force_login(self.user_follower)
        self.client_auth_following.force_login(self.user_following)

    def test_successful_follow(self):
        self.client_auth_follower.get(
            reverse('posts:profile_follow', args={self.user_following}),
        )
        follow_count = Follow.objects.count()
        self.assertEqual(Follow.objects.all().count(), follow_count)

    def test_successful_unfollow(self):
        self.client_auth_follower.get(
            reverse('posts:profile_follow', args={self.user_following}),
        )
        self.client_auth_follower.get(
            reverse('posts:profile_unfollow', args={self.user_following}),
        )
        follow_count = Follow.objects.count()
        self.assertEqual(Follow.objects.all().count(), follow_count)

    def test_self_subscription(self):
        self.client_auth_follower.get(
            reverse('posts:profile_follow', args={self.user_follower}),
        )
        follow_count = Follow.objects.count()
        self.assertEqual(Follow.objects.all().count(), follow_count)

    def test_double_follow(self):
        self.client_auth_follower.get(
            reverse('posts:profile_follow', args={self.user_following}),
        )
        self.client_auth_follower.get(
            reverse('posts:profile_follow', args={self.user_following}),
        )
        follow_count = Follow.objects.count()
        self.assertEqual(Follow.objects.all().count(), follow_count)

    def test_anonymous_follow(self):
        self.client = Client()
        self.client.get(
            reverse('posts:profile_follow', args={self.user_following}),
        )
        follow_count = Follow.objects.count()
        self.assertEqual(Follow.objects.all().count(), follow_count)

    def test_follow_to_anonymous(self):
        self.client = Client()
        self.client_auth_follower.get(
            reverse('posts:profile_follow', args={self.client}),
        )
        follow_count = Follow.objects.count()
        self.assertEqual(0, follow_count)
