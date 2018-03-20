from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, exceptions
from rest_framework.fields import SerializerMethodField

from column.models import Post
from member.models import ProfileImage, Profile
from member.models.user import WaitingRelation, Relation

__all__ = (
    'ProfileSerializer',
    'ProfileImageSerializer',
)


class ProfileSerializer(serializers.ModelSerializer):

    def get_nickname(self,obj):
        return obj.user.nickname

    def get_following(self, obj):
        return Relation.objects.filter(from_user=obj.user).count()

    def get_follower(self, obj):
        return Relation.objects.filter(to_user=obj.user).count()

    def get_post_count(self, obj):
        return Post.objects.filter(author=obj.user).count()

    def get_waiting(self, obj):
        return WaitingRelation.objects.filter(receive_user=obj.user).count()

    def get_image(self, obj):
        try:
            image = ProfileImage.objects.filter(user=obj.user).get()
            serializer = ProfileImageSerializer(image)
            if serializer:
                print(serializer.data)
                return serializer.data
            raise exceptions.ValidationError({"detail":"excepted error"})
        except ObjectDoesNotExist:
            data = {
                "image": {
                    "profile_image": "static/images/example/2_x20_.jpeg",
                    "cover_image": "static/images/example/1.jpeg"
                }
            }
            return data

    post_count = SerializerMethodField()
    follower = SerializerMethodField()
    following = SerializerMethodField()
    waiting = SerializerMethodField()
    image = SerializerMethodField()
    nickname = SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'nickname',
            'year',
            'month',
            'sex',
            'facebook',
            'instagram',
            'twitter',
            'age',
            'phone',
            'intro',
            'jobs',
            'subjects',
            'web',
            'region',
            'intro',
            'follower',
            'following',
            'post_count',
            'waiting',
            'image'
        )


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = (
            'profile_image',
            'cover_image'
        )
