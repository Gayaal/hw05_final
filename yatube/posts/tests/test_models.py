from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )

    def test_post_models_correct_names(self) -> None:
        self.assertEqual(
            self.post.text[: settings.CHARACTER_NUMBER], str(self.post),
        )


class GroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

    def test_group_models_correct_names(self) -> None:
        self.assertEqual(self.group.title, str(self.group))


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            text='Тестовый комментарий',
            author=cls.user,
        )

    def test_comment_models_correct_names(self) -> None:
        self.assertEqual(
            self.comment.text[: settings.CHARACTER_NUMBER],
            str(self.comment),
        )


class FollowModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user')
        cls.author = User.objects.create_user(username='author')
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.author,
        )

    def test_follow_models_correct_names(self) -> None:
        follow_str_value = self.follow.__str__()
        follow_test_value = self.follow.user.get_username()
        self.assertEqual(follow_str_value, follow_test_value)
        self.assertIsInstance(follow_str_value, str)
