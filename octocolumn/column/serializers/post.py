from rest_framework import serializers

from column.models import Temp
from column.models import TempFile
from ..serializers.comment import CommentSerializer
from ..models import Post


__all__ = (
    'PostSerializer',
    'TempSerializer',
    'TempFileSerializer'
)


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class PostSerializer(serializers.ModelSerializer):
    # 아래 코드가 동작하도록 CommentSerializer를 구현
    my_comment = CommentSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    cover_image = Base64ImageField(max_length=None, use_url=True)
    preview_image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'photo',
            'main_content',
            'my_comment',
            'comments',
            'cover_image',
            'preview_image'
        )
        read_only_fields = (
            'author',
            'my_comment',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['is_like'] = self.context['request'].user in instance.like_users.all()
        return ret


class TempSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title =serializers.CharField(allow_blank=True,max_length=255),

    class Meta:
        model = Temp
        fields = (
            'id',
            'title',
            'main_content',
            'author_id'

        )


class TempFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = TempFile
        fields = (
            'id',
            'file',
            'author_id'
        )













