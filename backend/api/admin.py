from api.v1.models import (Cart, Favorite, Ingredient, IngredientAmount,
                           Recipe, Tag)
from django.contrib import admin
from django.contrib.admin import ModelAdmin


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 0


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')


@admin.register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')


@admin.register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)


@admin.register(IngredientAmount)
class IngredientAmountAdmin(ModelAdmin):
    list_display = ('recipe', 'amount', 'units', 'ingredient_name')

    def ingredient_name(self, obj):
        return obj.ingredient.name

    def units(self, obj):
        return obj.ingredient.measurement_unit

    units.short_description = 'Единица измерения'
    ingredient_name.short_description = 'Ингредиент'


@admin.register(Recipe)
class RecipeAdmin(ModelAdmin):
    filter_horizontal = ('tags',)
    inlines = (IngredientInline,)
    list_display = (
        'name',
        'author',
        'count_favorites'
    )
    list_display_links = ('name',)
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name', 'author__username')

    def count_favorites(self, obj):
        return obj.favorites.count()

    count_favorites.short_description = 'В избранном'


@admin.register(Tag)
class Tag(ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
