from rest_framework import serializers

from column.models import SearchTag

__all__ =(
    'SearchTagSerializer',
)


class SearchTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTag
        fields = (
            'tag',
        )