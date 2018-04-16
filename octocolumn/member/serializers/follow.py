from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable
from rest_framework.fields import SerializerMethodField

from member.models import ProfileImage, Author, Profile
from member.models.user import Relation, User
from member.serializers import UserSerializer, ProfileImageSerializer, AuthorSerializer

__all__ = (
    'FollowStatusSerializer',
)


class FollowStatusSerializer(serializers.ModelSerializer):

    def image(self, user):
        try:
            img = ProfileImage.objects.select_related('user').filter(user=user).get()
            return ProfileImageSerializer(img).data
        except ObjectDoesNotExist:
            data = {
                'profile_image': 'https://devtestserver.s3.amazonaws.com/media/example/2_x20_.jpeg',
                'cover_image': 'https://devtestserver.s3.amazonaws.com/media/example/1.jpeg'
            }
            return data

    def get_follow_status(self, obj):
        user = self.context.get('request').user

        if obj == user:
            return 2
        try:
            Relation.objects.select_related('to_user', 'from_user').filter(to_user=obj, from_user=user).get()
            return True
        except ObjectDoesNotExist:
            return False

    def get_follower_count(self, obj):
        return Relation.objects.select_related('to_user__user').filter(to_user=obj).count()

    def get_user(self, obj):
        serializer = UserSerializer(obj)
        profile = Profile.objects.select_related('user').filter(user=obj).get()

        data = {
            "username": serializer.data['nickname'],
            "following_url": "/api/member/" + str(serializer.data['pk']) + "/follow/",
            "intro": profile.intro,
            "blog": '',
            "achevement": "",
            "instagram": profile.instagram,
            "facebook": profile.facebook,
            "twitter": profile.twitter,
            "img": self.image(obj)

        }

        return data
    user = SerializerMethodField()
    follow_status = SerializerMethodField()
    follower_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'user',
            'follow_status',
            'follower_count'
        )