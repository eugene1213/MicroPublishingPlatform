from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from ..models import Comment

__all__ = (
    'CommentSerializer',
)


class CommentSerializer(serializers.ModelSerializer):
    reply_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'post',
            'author',
            'content',
            'created_date',
            'reply_count',
            'parent_id',

        )
        read_only_fields = (
            'created_date',
        )

        def get_reply_count(self, obj):
            if obj.is_parent:
                return obj.children().count()
            return 0


class CommentChildSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'timestamp',
        ]