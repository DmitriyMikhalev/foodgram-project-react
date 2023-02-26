from .models import Cart, Favorite


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
