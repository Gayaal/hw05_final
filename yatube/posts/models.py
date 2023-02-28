from django.contrib.auth import get_user_model
from django.db import models

from yatube.settings import CHARACTER_NUMBER

User = get_user_model()


class Group(models.Model):
    title = models.CharField(verbose_name='Группа', max_length=200)
    slug = models.SlugField(verbose_name='Слаг', unique=True)
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name_plural = 'Группы'

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст', max_length=200)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Группа',
    )
    image = models.ImageField(
        verbose_name='Картинка', upload_to='posts/', blank=True
    )

    class Meta:
        default_related_name = 'posts'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:CHARACTER_NUMBER]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Комментарий',
        help_text='Прокомментируйте запись',
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
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.text[:CHARACTER_NUMBER]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-created',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'], name='unique_follow'
            )
        ]
