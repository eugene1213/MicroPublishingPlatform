from datetime import datetime

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from column.models import Temp
from column.models import TempFile
from ..serializers.comment import CommentSerializer
from ..models import Post


__all__ = (
    'PostSerializer',
    'TempSerializer',
    'TempFileSerializer',
    'PostListSerializer',
    'PreAuthorPostSerializer'
)


class PostSerializer(serializers.ModelSerializer):
    # 아래 코드가 동작하도록 CommentSerializer를 구현
    my_comment = CommentSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'main_content',
            'my_comment',
            'title',
            'created_date',
            'price',
            'comments',
            'cover_image',
            'preview_image',
        )
        read_only_fields = (
            'author',
            'my_comment',
        )

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     ret['is_like'] = self.context['request'].user in instance.like_users.all()
    #     return ret


class PostListSerializer(serializers.ModelSerializer):
    Post = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'main_content',
            'my_comment',
            'title',
            'created_date',
            'comments',
            'cover_image',
            'preview_image'
        )
        read_only_fields = (
            'author',
            'my_comment',
        )


class TempSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title =serializers.CharField(allow_blank=True,max_length=255),

    class Meta:
        model = Temp
        fields = (
            'id',
            'title',
            'main_content',
            'author_id'

        )


class TempFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = TempFile
        fields = (
            'id',
            'file',
            'author_id'
        )


class PreAuthorPostSerializer(serializers.ModelSerializer):
    # 아래 코드가 동작하도록 CommentSerializer를 구현
    my_comment = CommentSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'main_content',
            'title',
            'cover_image',
            'preview_image'
        )
