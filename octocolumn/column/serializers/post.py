import re
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, CurrentUserDefault

from column.models import Temp, SearchTag
from column.models import TempFile

from member.models import ProfileImage
from member.models.user import Relation
from member.serializers import UserSerializer, ProfileImageSerializer
from ..serializers.comment import CommentSerializer
from ..models import Post


__all__ = (
    'PostSerializer',
    'TempSerializer',
    'PostMoreSerializer',
    'TempFileSerializer',
    'PostListSerializer',
    'PreAuthorPostSerializer'
)


class PostSerializer(serializers.ModelSerializer):
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


class PostMoreSerializer(serializers.ModelSerializer):
    # 아래 코드가 동작하도록 CommentSerializer를 구현
    def follower_status(self, data):
        try:
            Relation.objects.filter(to_user=data, from_user=self.context.get('request').user).get()
            return True
        except ObjectDoesNotExist:
            return False

    def image(self, user):
        try:
            img = ProfileImage.objects.filter(user=user).get()
            return ProfileImageSerializer(img).data
        except ObjectDoesNotExist:
            data = {
                'profile_img': '/static/images/example/2.png',
                'cover_img': '/static/images/example/1.png'
            }
            return data

    def get_created_datetime(self,obj):
        return obj.created_date.strftime('%Y.%m.%d')+' '+obj.created_date.strftime('%H:%M')

    def get_typo_count(self, obj):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', obj.main_content)
        return len(clean_text) - clean_text.count(' ')/2

    def get_tag(self, obj):
        tag = SearchTag.objects.filter(post=obj)
        from column.serializers import SearchTagSerializer
        tag_serializer = SearchTagSerializer(tag, many=True)
        if tag_serializer:
            return tag_serializer.data
        return None

    def get_author(self,obj):
        serializer = UserSerializer(obj.author)
        data = {
            "author_id": serializer.data['pk'],
            "username": serializer.data['username'],
            "follow_status": self.follower_status(obj.author),
            "follower_count": Relation.objects.filter(to_user=obj.author).count(),
            "following_url": "/api/member/" + str(serializer.data['pk']) + "/follow/",
            "achevement": "",
            "img": self.image(obj.author)
        }

        return data

    my_comment = CommentSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    created_datetime = SerializerMethodField()
    typo_count = SerializerMethodField()
    tag = SerializerMethodField()

    author = SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'main_content',
            'my_comment',
            'title',
            'created_date',
            'created_datetime',
            'tag',
            'price',
            'comments',
            'cover_image',
            'preview_image',
            'typo_count'
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

    class Meta:
        model = Temp
        fields = (
            'id',
            'title',
            'main_content',
            'created_date',
            'author'

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
