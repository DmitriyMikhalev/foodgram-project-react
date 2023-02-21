from api.paginations import PageLimitPagination
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as BaseUserViewSet

User = get_user_model()


class UserViewSet(BaseUserViewSet):
    pagination_class = PageLimitPagination
