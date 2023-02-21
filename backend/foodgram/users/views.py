from api.paginations import PageLimitPagination
from djoser.views import UserViewSet as BaseUserViewSet
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(BaseUserViewSet):
    pagination_class = PageLimitPagination
