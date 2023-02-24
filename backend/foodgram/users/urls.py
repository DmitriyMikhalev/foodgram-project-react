from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import TokenCreateView, UserViewSet

router = DefaultRouter()
router.register(prefix='users', viewset=UserViewSet)

app_name = 'users'

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r"^auth/token/login/?$", TokenCreateView.as_view(), name="login"),
    path('auth/', include('djoser.urls.authtoken')),
]
