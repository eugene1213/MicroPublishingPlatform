from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from column.models import Post
from member.models import ProfileImage, Profile, User
from member.models.user import Relation

__all__ = (
    'ProfileSerializer',
    'ProfileImageSerializer',
)


class ProfileSerializer(serializers.ModelSerializer):
    def get_follower(self, obj):
        return obj.user.following_users.count()

    def get_following(self, obj):
        return Relation.objects.filter(from_user=obj.user).count()

    def get_post_count(self, obj):
        return Post.objects.filter(author=obj.user).count()

    def get_waiting(self, obj):
        return obj.user.waiting

    post_count = SerializerMethodField()
    follower = SerializerMethodField()
    following = SerializerMethodField()
    waiting = SerializerMethodField()

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
            'waiting'
        )


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = (
            'profile_image',
            'cover_image'
        )
