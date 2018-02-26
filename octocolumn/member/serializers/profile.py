from rest_framework import serializers

from member.models import Profile

__all__ =(
    'ProfileImageSerializer',
)


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'pk',
            'cover_image',
            'profile_image'
        )