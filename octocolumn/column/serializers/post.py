import re

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from column.models import Temp, SearchTag
from column.models import TempFile

from member.models import ProfileImage
from member.models.user import Bookmark
from member.serializers import UserSerializer, ProfileImageSerializer
from ..models import Post


__all__ = (
    'PostSerializer',
    'TempSerializer',
    'PostMoreSerializer',
    'TempFileSerializer',
    'PostListSerializer',
    'PreAuthorPostSerializer',
    'MyTempSerializer'
)


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'title',
            'created_date',
            'price',
            'main_content',
            'preview',
            'cover_image',
        )


class MyPublishPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'title',
            'created_date',
            'price',
            'preview',
            'cover_image',
        )


class PostMoreSerializer(serializers.ModelSerializer):
    def get_all_status(self, obj):
        user = self.context.get('request').user
        author_serializer = UserSerializer(obj.author)
        data = {
            "img": self.image(obj.author),
            # "created_datetime": obj.created_date.strftime('%Y.%m.%d')+' '+obj.created_date.strftime('%H:%M'),
            "created_date": obj.created_date.strftime('%B')[:3] + obj.created_date.strftime(' %d'),
            "typo_count": self.typo_count(obj),
            "author_id": author_serializer.data['pk'],
            "username": author_serializer.data['nickname'],
            # "following_url": "/api/member/" + str(author_serializer.data['pk']) + "/followStatus/",
            "achevement": "",
            "main_content": self.main_content(obj),
            "bookmark_status": self.bookmark_status(obj, user)
        }
        return data

    def image(self, author):
        try:
            img = ProfileImage.objects.select_related('user').filter(user=author).get()
            return {"profile_image" : ProfileImageSerializer(img).data['profile_image']}
        except ObjectDoesNotExist:
            data = {
                'profile_image': 'https://devtestserver.s3.amazonaws.com/media/example/2_x20_.jpeg',
                # 'cover_image': 'https://devtestserver.s3.amazonaws.com/media/example/1.jpeg'
            }
            return data
    #
    # def get_created_datetime(self,obj):
    #     return obj.created_date.strftime('%Y.%m.%d')+' '+obj.created_date.strftime('%H:%M')

    def typo_count(self, obj):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', obj.main_content)
        return len(clean_text) - clean_text.count(' ')/2

    # def get_tag(self, obj):
    #     tag = SearchTag.objects.select_related('post').filter(post=obj).all()
    #     from column.serializers import SearchTagSerializer
    #     tag_serializer = SearchTagSerializer(tag, many=True)
    #     if tag_serializer:
    #         return tag_serializer.data
    #     return None

    # def get_author(self, obj):
    #     serializer = UserSerializer(obj.author)
    #     data = {
    #         "author_id": serializer.data['pk'],
    #         "username": serializer.data['nickname'],
    #         "following_url": "/api/member/" + str(serializer.data['pk']) + "/followStatus/",
    #         "achevement": "",
    #         "img": self.image(obj.author)
    #     }
    #
    #     return data

    def main_content(self, obj):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', obj.main_content)
        return clean_text[:300]

    # def get_created_date(self, obj):
    #     return obj.created_date.strftime('%B')[:3] + obj.created_date.strftime(' %d')

    def bookmark_status(self, obj, user):
        if user.is_authenticated:
            try:
                Bookmark.objects.select_related('user', 'post').filter(user=user, post=obj).get()
                return True
            except ObjectDoesNotExist:
                return False
        return False

    # created_datetime = SerializerMethodField()
    # typo_count = SerializerMethodField()
    # tag = SerializerMethodField()
    # main_content = SerializerMethodField()
    # author = SerializerMethodField()
    # created_date = SerializerMethodField()
    # bookmark_status = SerializerMethodField()
    all_status = SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'pk',
            # 'author',
            # 'main_content',
            'title',
            # 'created_date',
            # 'created_datetime',
            # 'tag',
            'price',
            # 'cover_image',
            'thumbnail',
            'preview',
            # 'typo_count',
            # 'bookmark_status'
            'all_status',
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
            'title',
            'created_date',
            'cover_image',
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


class MyTempSerializer(serializers.ModelSerializer):

    class Meta:
        model = Temp
        fields = (
            'id',
            'title',
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
