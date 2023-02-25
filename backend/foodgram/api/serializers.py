from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator, ValidationError
from users.serializers import Base64ImageField, UserSerializer

from api.models import (Cart, Favorite, Ingredient, IngredientAmount, Recipe,
                        Tag)


class IngredientSerializer(ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit'
        )
        model = Ingredient


class IngredientAmountSerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )
        model = IngredientAmount
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientAmount.objects.all(),
                fields=('ingredient', 'recipe')
            )
        ]


class TagSerializer(ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
        model = Tag


class CartFavoriteFlagsMixin:
    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False

        return Favorite.objects.filter(recipe=obj, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False

        return Cart.objects.filter(recipe=obj, user=user).exists()


class ReadRecipeSerializer(ModelSerializer, CartFavoriteFlagsMixin):
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = IngredientAmountSerializer(
        many=True,
        source='ingredient_amount'
    )
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        read_only_fields = fields
        model = Recipe


class CreateRecipeSerializer(ModelSerializer, CartFavoriteFlagsMixin):
    id = ReadOnlyField()
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True,
        source='ingredient_amount',
        read_only=True
    )
    image = Base64ImageField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        model = Recipe

    def create(self, validated_data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')

        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredient_amount(objs=ingredients, recipe=recipe)

        return recipe

    @transaction.atomic
    def create_ingredient_amount(self, objs, recipe):
        IngredientAmount.objects.bulk_create(
            IngredientAmount(
                amount=ingrd['amount'],
                ingredient_id=ingrd['id'],
                recipe=recipe
            ) for ingrd in objs
        )

    def update(self, obj, validated_data):
        ingredients = self.initial_data.get('ingredients')
        if ingredients is not None:
            IngredientAmount.objects.filter(recipe=obj).delete()
            self.create_ingredient_amount(objs=ingredients, recipe=obj)

        tags = self.initial_data.get('tags')
        if tags is not None:
            obj.tags.clear()
            obj.tags.set(tags)

        obj.image = validated_data.get('image', obj.image)
        obj.name = validated_data.get('name', obj.name)
        obj.text = validated_data.get('text', obj.text)
        obj.cooking_time = validated_data.get('cooking_time', obj.cooking_time)
        obj.save()

        return obj

    def validate(self, data):
        initial_data = self.initial_data
        request = self.context['request']

        if request.method == 'POST':
            for field in ('tags', 'ingredients'):
                if initial_data.get(field) is None:
                    raise ValidationError(
                        detail={
                            f'{field}': 'Поле не может быть пустым.'
                        }
                    )
        data['author'] = request.user
        if ingredients := initial_data.get('ingredients'):
            self._validate_ingredients(
                ingredients=ingredients
            )
        if tags := initial_data.get('tags'):
            self._validate_tags(
                tags=tags
            )

        return data

    def _validate_tags(self, tags):
        if not isinstance(tags, list):
            raise ValidationError(
                detail={
                    'tags': 'Ожидался список тегов.'
                }
            )

        if len(tags) == 0:
            raise ValidationError(
                detail={
                    'tags': 'Рецепт должен иметь как минимум 1 тег.'
                }
            )

        used_tags = []
        for id in tags:
            if not isinstance(id, int):
                raise ValidationError(
                    detail={
                        'tags': 'Ожидались id тегов.'
                    }
                )

            tag = get_object_or_404(klass=Tag, pk=id)
            if tag in used_tags:
                raise ValidationError(
                    detail={
                        'tag': f'{tag} не может повторяться.'
                    }
                )

            used_tags.append(tag)

        return tags

    def _validate_ingredients(self, ingredients):
        if not isinstance(ingredients, list):
            raise ValidationError(
                detail={
                    'ingredients': 'Ожидался список.'
                }
            )

        if len(ingredients) == 0:
            raise ValidationError(
                detail={
                    'Рецепт должен иметь как минимум 1 ингредиент.'
                }
            )

        used_ingredients = []
        for item in ingredients:
            if not isinstance(item, dict):
                raise ValidationError(
                    detail={
                        'ingredients': 'Ожидались словари в списке.'
                    }
                )

            for key in ('id', 'amount'):
                if key not in item:
                    raise ValidationError(
                        detail={
                            'ingredients': f'Укажите {key} ингредиента.'
                        }
                    )

            ingredient = get_object_or_404(klass=Ingredient, pk=item['id'])
            if ingredient in used_ingredients:
                raise ValidationError(
                    detail={
                        'ingredients': f'{ingredient} не может повторяться.'
                    }
                )

            amount = item['amount']
            if amount < 1:
                raise ValidationError(
                    detail={
                        'ingredients': f'{ingredient}: неверное количество.'
                    }
                )

            used_ingredients.append(ingredient)

        return ingredients
