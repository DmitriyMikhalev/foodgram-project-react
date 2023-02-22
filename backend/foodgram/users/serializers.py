from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework.serializers import (ModelSerializer, ReadOnlyField,
                                        SerializerMethodField)

from .models import Follow

User = get_user_model()


class UserSerializer(BaseUserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        model = User

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_anonymous or request_user == obj:
            return False

        return Follow.objects.filter(user=request_user, author=obj).exists()


class FollowSerializer(ModelSerializer):
    email = ReadOnlyField(source='user.email')
    id = ReadOnlyField(source='user.id')
    username = ReadOnlyField(source='user.username')
    first_name = ReadOnlyField(source='user.first_name')
    last_name = ReadOnlyField(source='user.last_name')
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(author=obj.author, user=obj.user).exists()

    def get_recipes(self, obj):
        # TODO
        return []

    def get_recipes_count(self, obj):
        # TODO
        return 0
