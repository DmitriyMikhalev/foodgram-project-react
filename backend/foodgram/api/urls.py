from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet

router = DefaultRouter()
router.register(prefix='tags', viewset=TagViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
