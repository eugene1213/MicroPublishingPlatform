from rest_framework import serializers

from member.models import User


class SecondPasswordSerializer(serializers.ModelSerializer):
    second_password = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'user',
            'second_password'
        )



