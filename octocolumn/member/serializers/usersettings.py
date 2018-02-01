from rest_framework import serializers

from member.models import User


class SecondPasswordSerializer(serializers.ModelSerializer):
    second_password = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'second_password'
        )

    def validate(self, data):
        second_password = data['second_password']
        if type(second_password) is not int:
            raise serializers.ValidationError('숫자만 입력이 가능합니다.')
        return data

