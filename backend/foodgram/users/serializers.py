from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework.serializers import SerializerMethodField

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
