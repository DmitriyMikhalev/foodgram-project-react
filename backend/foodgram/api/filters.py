from django.contrib.auth import get_user_model
from django_filters import (AllValuesMultipleFilter, ChoiceFilter, FilterSet,
                            ModelChoiceFilter)

from .models import Recipe

User = get_user_model()

BOOLEAN_CHOICES = (
    (0, 'false',),
    (1, 'true',),
)


class RecipeFilter(FilterSet):
    author = ModelChoiceFilter(queryset=User.objects.all())
    tags = AllValuesMultipleFilter(
        conjoined=True,
        field_name='tags__slug'
    )
    is_favorited = ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        method='get_is_favorited'
    )
    is_in_shopping_cart = ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        value = int(value)

        if user.is_anonymous:
            return Recipe.objects.none() if value else queryset

        if value:
            return queryset.filter(favorites__user=user)

        return queryset.exclude(favorites__user=user)

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        value = int(value)

        if user.is_anonymous:
            return Recipe.objects.none() if value else queryset

        if value:
            return queryset.filter(carts__user=user)

        return queryset.exclude(carts__user=user)
