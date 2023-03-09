from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        verbose_name='заголовок',
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name='слаг',
        unique=True,
    )
    description = models.TextField(
        verbose_name='описание',
    )

    class Meta:
        verbose_name_plural = 'группы'

    def __str__(self) -> str:
        return self.title[: settings.CHARACTER_NUMBER]


class Post(models.Model):
    text = models.TextField(verbose_name='текст', max_length=200)
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='группа',
    )
    image = models.ImageField(
        verbose_name='картинка',
        upload_to='posts/',
        blank=True,
    )

    class Meta:
        default_related_name = 'posts'
        verbose_name_plural = 'посты'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[: settings.CHARACTER_NUMBER]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='комментарий',
        help_text='прокомментируйте запись',
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Комментатор',
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Введите комментарий',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан',
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.text[: settings.CHARACTER_NUMBER]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='подписчик',
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        related_name='following',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='создан',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        ordering = ('-created',)
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'user'),
                name='unique_follow',
            )
        ]

    def __str__(self) -> str:
        return self.user.get_username()
