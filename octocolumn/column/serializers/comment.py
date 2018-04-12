from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, exceptions
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from member.models import ProfileImage
from member.serializers import ProfileImageSerializer
from ..models import Comment

__all__ = (
    'CommentSerializer',
    'CommentChildSerializer',
    'CommentDetailSerializer'
)


class CommentSerializer(ModelSerializer):
    def child_all_count(self, data):
        sum = 0
        if data != None:
            for i in data:
                sum += i.children().count()
                return sum
        return 0

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count() + self.child_all_count(obj.children())
        return 0

    def get_my_comment(self, obj):
        if self.context.get('request').user.is_authenticated:
            user = self.context.get('request').user
            if obj.author == user:
                return True
            return False
        return False

    def get_image(self, obj):
        try:
            image = ProfileImage.objects.filter(user=obj.author).get()
            serializer = ProfileImageSerializer(image)
            if serializer:
                return serializer.data
            raise exceptions.ValidationError({"detail": "excepted error"})
        except ObjectDoesNotExist:
            data = {
                "image": {
                    "profile_image": "https://devtestserver.s3.amazonaws.com//media/example/2_x20_.jpeg",
                    "cover_image": "https://devtestserver.s3.amazonaws.com//media/example/1.jpeg"
                }
            }
            return data

    # def get_like_url(self, obj):
    #     return "/api/column/" + str(obj.pk) + "/comment-like/"

    reply_count = SerializerMethodField()
    # like_url = SerializerMethodField()
    my_comment = SerializerMethodField()
    image = SerializerMethodField()
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
            'my_comment',
            'parent_id',
            'image',
            # 'like_url'
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

