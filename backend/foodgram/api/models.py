from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint
from foodgram.settings import (COLORFIELD_LENGTH, MAX_CHARFIELD_LENGTH,
                               MIN_COOKING_TIME)
from users.models import User


class Cart(models.Model):
    user = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='carts',
        to=User,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='carts',
        to='Recipe',
        verbose_name='Рецепт'
    )

    class Meta:
        constraint = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='Этот рецепт уже добавлен в корзину.'
            )
        ]
        ordering = ('-id',)
        verbose_name = 'Корзина'


class Favorite(models.Model):
    user = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='favorites',
        to=User,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='favorites',
        to='Recipe',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ('-id',),
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=MAX_CHARFIELD_LENGTH,
        verbose_name='Название ингредиента'
    )
    units = models.CharField(
        max_length=15,
        verbose_name='Единицы измерения'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Ингрединт'
        verbose_name_plural = 'Ингрединты'


class IngredientAmount(models.Model):
    amount = models.IntegerField(
        verbose_name='Количество'
    )
    ingredient = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='ingredients',
        to='Ingredient',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='recipes',
        to='Recipe',
        verbose_name='Рецепт'
    )


class Tag:
    color = models.CharField(
        default='#000000',
        max_length=COLORFIELD_LENGTH,
        unique=True,
        validators=(
            RegexValidator(regex=r'^#([A-Fa-f0-9]{6})$'),
        ),
    )
    name = models.CharField(
        max_length=MAX_CHARFIELD_LENGTH,
        verbose_name='Тег'
    )
    slug = models.SlugField()


class Recipe(models.Model):
    author = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='recipes',
        to=User,
        verbose_name='Автор рецепта'
    )
    tags = models.ManyToManyField(to=Tag)
    ingredients = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='recipes',
        to='Ingredient',
        verbose_name='Ингредиенты'
    )
    image = ...        # base64
    name = models.CharField(
        max_length=MAX_CHARFIELD_LENGTH,
        verbose_name='Название рецепта'
    )
    text = models.TextField()
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                limit_value=MIN_COOKING_TIME,
                message='Проверте, что время приготовления составляет '
                        + 'не менее 1 минуты.'
            ),
        ),
        verbose_name='Время приготовления'
    )

    class Meta:
        ordering = ('-id', 'tags')
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

