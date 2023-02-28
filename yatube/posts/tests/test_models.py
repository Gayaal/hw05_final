from django.contrib.auth import get_user_model
from django.test import TestCase
from posts.models import Group, Post

from yatube.settings import CHARACTER_NUMBER

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )

    def test_models_have_correct_object_names(self) -> None:
        self.assertEqual(self.post.text[:CHARACTER_NUMBER], str(self.post))


class GroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

    def test_models_have_correct_object_names(self) -> None:
        self.assertEqual(self.group.title, str(self.group))
