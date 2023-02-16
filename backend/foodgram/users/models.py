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
        ordering = (models.F('author').desc(nulls_last=True),)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'user',),
                name='follow exists'
            ),
            models.CheckConstraint(
                check=models.Q(~(models.F('author') == models.F('user'))),
                name='self follow is not accessed'
            )
        ]
