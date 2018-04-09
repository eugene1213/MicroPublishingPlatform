from rest_framework import serializers

from member.models import User

__all__ = (
    'OctoCodeSerializer',
)


class OctoCodeSerializer(serializers.ModelSerializer):
    octo_code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'user',
            'second_password'
        )


    def validate(self, attrs):

        pass
