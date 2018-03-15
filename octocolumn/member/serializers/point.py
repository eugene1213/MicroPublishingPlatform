from rest_framework import serializers

from column.serializers import PostSerializer
from member.models import PointHistory


class PointHistorySerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = PointHistory
        fields = (
            'point',
            'history',
            'post',
            'point_use_type',
            'plus_minus',
            'created_at'
        )