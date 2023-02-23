from django.contrib import admin

from .models import Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag

admin.site.register(Cart)
admin.site.register(Favorite)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
admin.site.register(Recipe)
admin.site.register(Tag)
