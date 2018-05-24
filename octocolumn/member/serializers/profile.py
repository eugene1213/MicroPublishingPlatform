from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, exceptions
from rest_framework.fields import SerializerMethodField

from column.models import Post
from member.models import ProfileImage, Profile, UserSettings
from member.models.user import WaitingRelation, Relation

__all__ = (
    'ProfileMainSerializer',
    'ProfileImageSerializer',
    'ProfileSubSerializer',
)


class ProfileMainSerializer(serializers.ModelSerializer):

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
                return serializer.data
            raise exceptions.ValidationError({"detail": "excepted error"})
        except ObjectDoesNotExist:
            data = {

                    "profile_image": "https://static.octocolumn.com/media/example/2_x20_.jpeg",
                    "cover_image": "https://static.octocolumn.com/media/example/1.jpeg"
            }
            return data

    # def get_birth_day(self, obj):
    #     return str(obj.month) + '/' + str(obj.day) + '/' + str(obj.year)

    post_count = SerializerMethodField()
    follower = SerializerMethodField()
    following = SerializerMethodField()
    waiting = SerializerMethodField()
    image = SerializerMethodField()
    nickname = SerializerMethodField()
    # birth_day = SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'nickname',
            'facebook',
            'instagram',
            'twitter',
            'web',
            'intro',
            'follower',
            'following',
            'post_count',
            'waiting',
            'image'
        )


class ProfileSubSerializer(serializers.ModelSerializer):
    def get_username(self,obj):
        return obj.user.username
    
    def get_settings(self,obj):
        try:
            settings = UserSettings.objects.filter(user=obj.user).get()

            data = {
                    "phone": settings.phone,
                    "email": settings.email,
                    "facebook": settings.facebook,
                    "web": settings.web,
                    "sex": settings.sex,
                    "instagram": settings.instagram,
                    "birthday": settings.birthday,
                    "twitter": settings.twitter,
                    "jobs": settings.jobs,
                    "interest": settings.subjects

                }
            return data
        except ObjectDoesNotExist:
            user_settings = UserSettings.objects.create(user=obj.user)
            data = {
                "phone": user_settings.phone,
                "email": user_settings.email,
                "facebook": user_settings.facebook,
                "web": user_settings.web,
                "sex": user_settings.sex,
                "instagram": user_settings.instagram,
                "birthday": user_settings.birthday,
                "jobs": user_settings.jobs,
                "twitter": user_settings.twitter,
                "interest": user_settings.subjects

            }

            return data

    username = SerializerMethodField()
    settings = SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'username',
            'sex',
            'birthday',
            'phone',
            'jobs',
            'subjects',
            'intro',
            'settings'
        )


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = (
            'profile_image',
            'cover_image'
        )
