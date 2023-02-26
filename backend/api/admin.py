from api.v1.models import (Cart, Favorite, Ingredient, IngredientAmount,
                           Recipe, Tag)
from django.contrib import admin
from django.contrib.admin import ModelAdmin


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'text',
        'cooking_time',
    )
    filter_horizontal = ('tags',)
    inlines = (IngredientInline,)


admin.site.register(Cart)
admin.site.register(Favorite)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
admin.site.register(Tag)
