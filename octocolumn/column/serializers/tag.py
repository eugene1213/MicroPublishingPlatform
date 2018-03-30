from rest_framework import serializers

from column.models import SearchTag, PreSearchTag

__all__ =(
    'SearchTagSerializer',
    'PreSearchTagSerializer',
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