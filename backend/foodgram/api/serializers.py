from rest_framework.serializers import ModelSerializer

from .models import Tag


class TagSerializer(ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
        model = Tag