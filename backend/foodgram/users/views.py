from api.paginations import PageLimitPagination
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser import utils
from djoser.conf import settings as djoser_settings
from djoser.views import TokenCreateView as BaseTokenCreateView
from djoser.views import UserViewSet as BaseUserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from users.models import Follow
from users.serializers import FollowSerializer

User = get_user_model()


class TokenCreateView(BaseTokenCreateView):
    """Default djoser view, but changed status from HTTP_200 to HTTP_201."""
    serializer_class = djoser_settings.SERIALIZERS.token_create
    permission_classes = djoser_settings.PERMISSIONS.token_create

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = djoser_settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data, status=HTTP_201_CREATED
        )


class UserViewSet(BaseUserViewSet):
    pagination_class = PageLimitPagination

    @action(methods=['get'], detail=False)
    def me(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                data={'detail': 'Учетные данные не были предоставлены.'}
            )

        return super().me(request, *args, **kwargs)

    @action(detail=True, methods=['DELETE', 'POST'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        """user - кто, author - на кого"""
        kwargs = {
            'author': get_object_or_404(klass=User, pk=id),
            'user': request.user
        }

        if kwargs['user'] == kwargs['author']:
            return Response(
                data={
                    'errors': 'Нельзя подписаться или отписаться от себя.'
                },
                status=HTTP_400_BAD_REQUEST
            )

        if request.method == 'POST':
            if Follow.objects.filter(**kwargs).exists():
                return Response(
                    data={'errors': 'Подписка уже существует.'},
                    status=HTTP_400_BAD_REQUEST
                )

            subscription = Follow.objects.create(**kwargs)
            serializer = FollowSerializer(
                context={'request': request},
                instance=subscription
            )
            return Response(data=serializer.data, status=HTTP_201_CREATED)

        if (subscription := Follow.objects.filter(**kwargs)).exists():
            subscription.delete()
            return Response(status=HTTP_204_NO_CONTENT)

        return Response(
            data={'errors': 'Вы не подписаны на этого пользователя.'},
            status=HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['GET'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        subsriptions = Follow.objects.filter(user=request.user)
        paginated_queryset = self.paginate_queryset(subsriptions)
        serializer = FollowSerializer(
            context={'request': request},
            instance=paginated_queryset,
            many=True
        )

        return self.get_paginated_response(data=serializer.data)
