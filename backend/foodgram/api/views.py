from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.serializers import RecipeMinifiedSerializer

from api.models import Favorite, Ingredient, Recipe, Tag, Cart
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (IngredientSerializer, RecipeSerializer,
                             TagSerializer)


class IngredientViewSet(ReadOnlyModelViewSet):
    filter_backends = (SearchFilter,)
    pagination_class = None
    permission_classes = (AllowAny,)
    search_fields = ('^name',)
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    @action(methods=['DELETE', 'POST'], detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        user = request.user
        obj = Favorite.objects.filter(user=user, recipe__pk=pk)
        if request.method == 'DELETE':
            if not obj.exists():
                return Response(
                    data={'errors': 'Рецепт не находится в избранном.'},
                    status=HTTP_400_BAD_REQUEST
                )

            obj.delete()
            return Response(status=HTTP_204_NO_CONTENT)

        if obj.exists():
            return Response(
                data={'errors': 'Рецепт уже находится в избранном.'},
                status=HTTP_400_BAD_REQUEST
            )

        recipe = Recipe.objects.get(pk=pk)
        Favorite.objects.create(user=user, recipe=recipe)
        return Response(
            data=RecipeMinifiedSerializer(instance=recipe).data,
            status=HTTP_201_CREATED
        )

    @action(methods=['DELETE', 'POST'], detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        user = request.user
        obj = Cart.objects.filter(recipe__pk=pk, user=user)
        if request.method == 'DELETE':
            if not obj.exists():
                return Response(
                    data={'errors': 'Рецепт не находится в коризне.'}
                )
            obj.delete()
            return Response(status=HTTP_204_NO_CONTENT)

        if obj.exists():
            return Response(
                data={'errors': 'Рецепт уже находится в корзине.'},
                status=HTTP_400_BAD_REQUEST
            )

        recipe = Recipe.objects.get(pk=pk)
        Cart.objects.create(user=user, recipe=recipe)
        return Response(
            data=RecipeMinifiedSerializer(instance=recipe).data,
            status=HTTP_201_CREATED
        )


class TagViewSet(ReadOnlyModelViewSet):
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
