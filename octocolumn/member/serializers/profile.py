from rest_framework import serializers

from member.models import ProfileImage

__all__ =(
    'ProfileImageSerializer',
)


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = (
            'pk',
            'profile_image',
            'cover_image'
        )
