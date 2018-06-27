from rest_framework import serializers

from member.models import Notification

__all__ = (
    'NotificationSerializer',
)


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = (
            # 'pk',
            # 'post',
            'comment',
            'contents',
            'read_status',
            'created_at'
        )