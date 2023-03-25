from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseModel(models.Model):
    text = models.TextField(
        verbose_name='текст',
        max_length=200,
    )
    author = models.ForeignKey(
        User,
        verbose_name='автор',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True,
        null=True,
    )

    class Meta:
        abstract = True
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.text[: settings.CHARACTER_NUMBER]


class CreatedModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='создан',
    )

    class Meta:
        abstract = True
        ordering = ('-created',)
