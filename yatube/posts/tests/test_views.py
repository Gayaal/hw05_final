# from django import forms
from django.contrib.auth import get_user_model
# from django.test import Client, TestCase
# from django.urls import reverse
# from posts.forms import PostForm
# from posts.models import Follow, Group, Post

User = get_user_model()

'''

class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post_with_group = Post.objects.create(
            author=cls.user,
            text='Пост с группой',
            group=cls.group,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def post_exist(self, response, group=False):
        if 'page_obj' in response.context:
            post = response.context['page_obj'][0]
        else:
            post = response.context['post']
        self.assertEqual(post.author, self.post.author)
        if group:
            self.assertEqual(post.text, self.post_with_group.text)
            self.assertEqual(post.group.title, self.group.title)
            self.assertEqual(post.group.description, self.group.description)
            return
        self.assertEqual(post.text, self.post.text)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list', args={self.group.slug}
            ): 'posts/group_list.html',
            reverse('posts:profile', args={self.user}): 'posts/profile.html',
            reverse(
                'posts:post_detail', args={self.post.pk}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit', args={self.post.pk}
            ): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.post_exist(response)

    def test_group_list_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:group_list', args={self.group.slug})
        )
        self.post_exist(response, True)

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:profile', args={self.user})
        )
        self.post_exist(response)

    def test_post_detail_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_detail', args={self.post_with_group.pk})
        )
        self.post_exist(response, True)

    def test_post_create_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertIsInstance(response.context.get('form'), PostForm)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'pk': f'{self.post.pk}'})
        )
        self.assertIsInstance(response.context.get('is_edit'), bool)
        self.assertEqual(response.context.get('is_edit'), True)
        self.assertIsInstance(response.context.get('form'), PostForm)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)


class FollowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='Author')
        cls.follower = User.objects.create_user(username='Follower')
        cls.user = User.objects.create_user(username='Unfollower')

    def test_authorized_client_follow(self):
        self.author_client = Client()
        self.author_client.force_login(self.author)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        follow_count = Follow.objects.count()
        self.assertRedirects(
            reverse('posts:profile_follow', args={self.author}),
            reverse('posts:profile', args={self.author}),
        )
        self.assertEqual(Follow.objects.count(), follow_count + 1)
        self.assertTrue(
            Follow.objects.filter(author__following__user=self.user).exists()
        )

    def test_authorized_client_unfollow(self):
        self.author_client = Client()
        self.author_client.force_login(self.author)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        follow_count = Follow.objects.count()
        self.assertRedirects(
            reverse('posts:profile_unfollow', args={self.author}),
            reverse('posts:profile', args={self.author}),
        )
        self.assertEqual(Follow.objects.count(), follow_count)
        self.assertFalse(
            Follow.objects.filter(author__following__user=self.user).exists()
        )

    def test_following_posts(self):
        self.author_client = Client()
        self.author_client.force_login(self.author)
        self.follower_client = Client()
        self.follower_client.force_login(self.follower)
        new_post = Post.objects.create(
            author=self.author,
            text='Только для подписчиков',
        )
        self.follower_client.post(
            reverse('posts:profile_follow', args={self.author}),
        )
        response = self.follower_client.get(reverse('posts:follow_index'))
        first_post = response.context['page_obj'][0]
        self.assertTrue(first_post == new_post)

    def test_unfollowing_posts(self):
        Post.objects.create(
            author=self.author,
            text='Только для подписчиков',
        )
        self.follower_client.post(
            reverse('posts:profile_follow', args={self.author})
        )
        response = self.authorized_client.get(reverse('posts:follow_index'))
        self.assertTrue(len(response.context['page_obj']) == 0)
'''
