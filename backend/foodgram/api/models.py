from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='recipes',
        to=User,
        verbose_name='Автор рецепта'
    )
    tags = ...         # ManyToMany to Tag
    ingredients = ...  # FK to Ingredient
    image = ...        # base64
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    text = models.TextField()
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Проверте, что время приготовления составляет '
                        + 'не менее 1 минуты.'
            )
        ]
    )
