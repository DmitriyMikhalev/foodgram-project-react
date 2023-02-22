from api.paginations import PageLimitPagination
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as BaseUserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from .models import Follow
from .serializers import FollowSerializer

User = get_user_model()


class UserViewSet(BaseUserViewSet):
    pagination_class = PageLimitPagination

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
            serializer = FollowSerializer(instance=subscription)
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
        serializer = FollowSerializer(instance=paginated_queryset, many=True)

        return self.get_paginated_response(data=serializer.data)
