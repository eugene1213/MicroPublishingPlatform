from rest_framework import serializers

from member.models import Author as AuthorModel
from member.serializers import UserSerializer

__all__ = (
    'AuthorSerializer',
)


class AuthorSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = AuthorModel
        fields = (
            'pk',
            'author',
            'is_active',
            'intro',
            'blog',
            'created_at'
        )


