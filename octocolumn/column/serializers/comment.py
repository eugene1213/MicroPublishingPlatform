from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from ..models import Comment

__all__ = (
    'CommentSerializer',
    'CommentChildSerializer',
    'CommentDetailSerializer'
)


class CommentSerializer(ModelSerializer):
    def child_all_count(self, data):
        sum = 0
        for i in data:
            sum += i.children().count()
            return sum

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count() + self.child_all_count(obj.children())
            # return obj.children().count()
        return 0

    reply_count = SerializerMethodField()
    username = serializers.CharField(source='author.nickname')

    class Meta:
        model = Comment
        fields = (
            'pk',
            'post',
            'username',
            'content',
            'created_date',
            'reply_count',
            'parent_id',

        )
        read_only_fields = (
            'created_date',
        )


class CommentChildSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'pk',
            'content',
            'created_date',
    )


class CommentDetailSerializer(ModelSerializer):

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def child_all_count(self, data):
        sum = 0
        for i in data:
            sum += i.children().count()
            return sum

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count() + self.child_all_count(obj.children())
            # return obj.children().count()
        return 0

    reply_count = SerializerMethodField()
    replies = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'pk',
            'content_type',
            'object_id',
            'content',
            'reply_count',
            'replies',
            'created_date',
        ]

