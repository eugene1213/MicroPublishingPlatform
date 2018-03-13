from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, exceptions
from rest_framework.fields import SerializerMethodField

from column.models import Post
from member.models import ProfileImage, Profile
from member.models.user import Relation

__all__ = (
    'ProfileSerializer',
    'ProfileImageSerializer',
)


class ProfileSerializer(serializers.ModelSerializer):
    def get_following(self, obj):
        return obj.user.following_users_count

    def get_follower(self, obj):
        return obj.user.follower_users_count

    def get_post_count(self, obj):
        return Post.objects.filter(author=obj.user).count()

    def get_waiting(self, obj):
        return obj.user.waiting_count

    def get_image(self, obj):
        try:
            image = ProfileImage.objects.filter(user=obj.user).get()
            serializer = ProfileImageSerializer(image)
            if serializer:
                return serializer.data
            raise exceptions.ValidationError({"detail":"excepted error"})
        except ObjectDoesNotExist:
            return None

    post_count = SerializerMethodField()
    follower = SerializerMethodField()
    following = SerializerMethodField()
    waiting = SerializerMethodField()
    image = SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'birth',
            'sex',
            'phone',
            'intro',
            'jobs',
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
