from rest_framework import serializers

from column.models import SearchTag, PreSearchTag, Tag

__all__ =(
    'TagSerializer',
    'SearchTagSerializer',
    'PreSearchTagSerializer',
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'tags',
        )

class SearchTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTag
        fields = (
            'tag',
        )


class PreSearchTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreSearchTag
        fields = (
            'tag',
        )