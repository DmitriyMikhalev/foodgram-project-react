from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(ReadOnlyModelViewSet):
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
