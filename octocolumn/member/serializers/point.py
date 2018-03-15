from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from column.serializers import PostSerializer
from member.models import PointHistory


class PointHistorySerializer(serializers.ModelSerializer):
    def get_plus_minus(self, obj):
        if obj.point_use_type == 'Buy':
            return -1
        if obj.point_use_type == 'Charge':
            return 1
        if obj.point_use_type == 'Reward':
            return 1
        if obj.point_use_type == 'Publish':
            return -1

    post = PostSerializer()
    plus_minus = SerializerMethodField()

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