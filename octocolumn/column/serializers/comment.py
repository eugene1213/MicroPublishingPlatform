from rest_framework import serializers

from ..models import Comment

__all__ = (
    'CommentSerializer',
)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'post',
            'author',
            'content',
            'created_date',
            'parent_id',

        )
        read_only_fields = (
            'created_date',
        )