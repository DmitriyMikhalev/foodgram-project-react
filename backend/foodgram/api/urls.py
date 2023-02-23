from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, TagViewSet

router = DefaultRouter()
router.register(prefix='ingredients', viewset=IngredientViewSet)
router.register(prefix='tags', viewset=TagViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
