from rest_framework import serializers

from member.models import ProfileImage

__all__ =(
    'ProfileImageSerializer',
    'CoverImageSerializer'
)


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = (
            'pk',
            'profile_image'
        )


class CoverImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = (
            'pk',
            'cover_image'
        )