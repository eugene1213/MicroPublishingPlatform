from rest_framework import serializers

from member.models import ProfileImage, Profile

__all__ = (
    'ProfileSerializer',
    'ProfileImageSerializer',
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'birth',
            'sex',
            'phone',
            'intro',
            'jobs',
            'intro'
        )


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = (
            'profile_image',
            'cover_image'
        )
