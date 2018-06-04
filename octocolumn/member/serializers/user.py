from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from member.models import User, Profile, ProfileImage
from member.task import SignupEmailTask
from utils.customsendmail import signup_email_send

__all__=(
    'UserSerializer',
    'SignUpSerializer',
    'ChangePasswordSerializer'
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'last_name',
            'first_name',
            'username',
            'nickname',
            'point',
            'is_active',
        )


class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    nickname = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password1',
            'password2',
            'nickname',
        )

    def validate(self, data):
        if data['password1'] != data['password2']:
            return serializers.ValidationError('비밀번호가 일치하지 않습니다.')

        if len(data['password1']) < 8:
            return serializers.ValidationError('비밀번호는 최소 8자리 입니다.')

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
           username=validated_data['username'],
           password=validated_data['password1'],
           nickname=validated_data['nickname'],
        )
        if user:
            task = SignupEmailTask

            if task.delay(user.pk):
                return user
            else:
                raise serializers.ValidationError('치명적인 오류입니다')

        else:
            raise serializers.ValidationError('이메일을 다시한번 확인해주시기 바랍니다.')

    def to_representation(self, instance):
        # serializer된 형태를 결정
        # super().to_representation()은 serialize된 기본 형태(dict)
        ret = super().to_representation(instance)
        data = {
            'user': ret,
        }
        # 마지막엔 serializer.data를 출력했을 때 반환될 값을 반환해줘야 함
        return data


class ChangePasswordSerializer(serializers.Serializer):

    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다')
        return data


