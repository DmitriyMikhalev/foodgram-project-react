from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Follow(models.Model):
    author = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='following',
        to=User,
        verbose_name='Автор'
    )
    user = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='follower',
        to=User,
        verbose_name='Подписчик'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'user',),
                name='Подписка уже существует.'
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F("user")),
                name='Подписка на самого себя не разрешена.'
            )
        ]
        ordering = ('author', 'user')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
