from rest_framework import serializers

from column.models import SearchTag, PreSearchTag, Tag, Recommend

__all__ =(
    'TagSerializer',
    'SearchTagSerializer',
    'PreSearchTagSerializer',
    'RecommendSerializer'
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


class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommend
        fields = (
            'text',
        )


class PreSearchTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreSearchTag
        fields = (
            'tag',
        )