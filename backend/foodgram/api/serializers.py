from django.shortcuts import get_object_or_404
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.validators import ValidationError
from users.serializers import Base64ImageField, UserSerializer

from .models import Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag


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


class TagSerializer(ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
        model = Tag


class RecipeSerializer(ModelSerializer):
    id = ReadOnlyField()
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True,
        source='ingredient_amount'
    )
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

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
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        tags = self.initial_data.get('tags')
        recipe.tags.set(tags)
        self.create_ingredient_amount(objs=ingredients, recipe=recipe)

    def create_ingredient_amount(self, objs, recipe):
        IngredientAmount.objects.bulk_create(
            IngredientAmount(
                amount=ingrd['amount'],
                ingredient=Ingredient.objects.get(id=ingrd['id']),
                recipe=recipe
            ) for ingrd in objs
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False

        return Favorite.objects.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False

        return Cart.objects.filter(recipe=obj, user=user).exists()

    def update(self, instance, validated_data):
        ingredients = validated_data.get(
            'ingredients',
            instance.ingredients
        )
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.create_ingredient_amount(objs=ingredients, recipe=instance)
        tags = self.initial_data.get(
            'tags'
        )
        instance.tags.clear()
        instance.tags.set(tags)
        instance.image = validated_data.get(
            'image',
            instance.image
        )
        instance.name = validated_data.get(
            'name',
            instance.name
        )
        instance.text = validated_data.get(
            'text',
            instance.text
        )
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.save()

        return instance

    def validate(self, data):
        if 'ingredients' not in self.initial_data:
            raise ValidationError(
                detail={'ingredients': 'Поле не может быть пустым.'}
            )
        used_ingredients = []
        for item in data['ingredients']:
            ingredient = get_object_or_404(klass=Ingredient, pk=item['id'])
            if ingredient in used_ingredients:
                raise ValidationError(
                    detail={'ingredients': f'Ингредиент {ingredient}'
                                           + ' не может повторяться.'}
                )
            amount = ingredient['amount']
            if not amount.isdigit() or amount == '0':
                raise ValidationError(
                    detail={'ingredients': f'{ingredient}: проверьте'
                                           + 'количество (от 1).'}
                )
            used_ingredients.append(ingredient)

        return data
