from django.db.models import F, QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.serializers import RecipeMinifiedSerializer

from .filters import RecipeFilter
from .models import Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag
from .permissions import IsOwnerOrReadOnly
from .serializers import (CreateRecipeSerializer, IngredientSerializer,
                          ReadRecipeSerializer, TagSerializer)


class IngredientViewSet(ReadOnlyModelViewSet):
    filter_backends = (SearchFilter,)
    pagination_class = None
    permission_classes = (AllowAny,)
    search_fields = ('^name',)
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadRecipeSerializer

        return CreateRecipeSerializer

    def _create_object(self, model, request, recipe_pk):
        user = request.user
        obj = model.objects.filter(recipe__pk=recipe_pk, user=user)

        if obj.exists():
            return Response(
                data={
                    'errors': f'{model._meta.verbose_name}: рецепт уже'
                              + ' добавлен.'
                },
                status=HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(klass=Recipe, pk=recipe_pk)
        model.objects.create(recipe=recipe, user=user)

        return Response(
            data=RecipeMinifiedSerializer(instance=recipe).data,
            status=HTTP_201_CREATED
        )

    def _delete_object(self, model, request, recipe_pk):
        user = request.user
        obj = model.objects.filter(recipe__pk=recipe_pk, user=user)

        if not obj.exists():
            return Response(
                data={
                    'errors': f'{model._meta.verbose_name}: рецепт не найден.'
                },
                status=HTTP_400_BAD_REQUEST
            )
        obj.delete()

        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['DELETE', 'POST'], detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self._obj_operation(
            model=Favorite,
            request=request,
            recipe_pk=pk
        )

    def _obj_operation(self, **kwargs):
        if kwargs['request'].method == 'DELETE':
            return self._delete_object(**kwargs)

        return self._create_object(**kwargs)

    @action(methods=['DELETE', 'POST'], detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self._obj_operation(
            model=Cart,
            request=request,
            recipe_pk=pk
        )

    @action(methods=['GET'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """
        <QuerySet [
            {
                'amount': 10,
                'name': 'овощи',
                'units': 'г'
            },
            {
                'amount': 15,
                'name': 'сахар',
                'units': 'г'
            }
        ]>
        """
        ingredients: QuerySet[dict] = IngredientAmount.objects.filter(
            recipe__carts__user=request.user
        ).values(
            'amount',
            name=F('ingredient__name'),
            units=F('ingredient__measurement_unit')
        )
        result = {}

        for ingrd_dict in ingredients:
            if (ingredient := ingrd_dict['name']) not in result:
                result[ingredient] = {
                    'amount': ingrd_dict['amount'],
                    'units': ingrd_dict['units']
                }
            else:
                result[ingredient]['amount'] += ingrd_dict['amount']

        if not result:
            return Response(
                data={
                    'errors': 'Корзина пуста.'
                },
                status=HTTP_400_BAD_REQUEST
            )

        shopping_list = ['Список ингредиентов к покупке:']
        for key, value in result.items():
            amount = value['amount']
            units = value['units']
            shopping_list.append(f'\n* {key}: {amount} {units}')

        shopping_list = ''.join(shopping_list)
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=shop_list.txt'

        return response


class TagViewSet(ReadOnlyModelViewSet):
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
