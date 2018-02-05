from rest_framework import serializers

from member.models import Profile

__all__ =(
    'ProfileImageSerializer',
)


class ProfileImageSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True)

    class Meta:
        model = Profile
        fields = (
            'file'
        )