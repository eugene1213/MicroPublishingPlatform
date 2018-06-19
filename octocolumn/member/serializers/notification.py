from rest_framework import serializers

from member.models import User
from member.models.notification import Notification
from member.serializers import UserSerializer


class NotificationSerializer(serializers.Serializer):
    recipient = UserSerializer(User, read_only=True)
    unread = serializers.BooleanField(read_only=True)

    class Meta:
        model = Notification
        fields = (
            'recipient',
            'unread',
        )