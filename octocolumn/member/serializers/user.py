from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from member.models import User
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
            'point',
            'is_active',
        )


class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name'
        )

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_type='d'
            # img_profile=validated_data.get('img_profile')
        )

        if user:
            email = signup_email_send(user)
            if not email:
                raise serializers.ValidationError('이메일 발송에 실패하였습니다.')
        else:
            raise serializers.ValidationError('이메일을 다시한번 확인해주시기 바랍니다.')

        return user

    def to_representation(self, instance):
        # serializer된 형태를 결정
        # super().to_representation()은 serialize된 기본 형태(dict)
        ret = super().to_representation(instance)
        data = {
            'user': ret,
            'token': instance.token,
        }
        # 마지막엔 serializer.data를 출력했을 때 반환될 값을 반환해줘야 함
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
