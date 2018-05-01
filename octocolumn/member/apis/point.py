from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from member.models import PointHistory
from member.pagination import PointHistoryPagination
from member.serializers.point import PointHistorySerializer


# 1
# 유저의 포인트 사용내역을 가져오는 API
# URL /api/member/getPointHistory/
class UserPointHistory(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PointHistoryPagination

    def list(self, request, *args, **kwargs):
        user = self.request.user
        try:
            # point = PointHistory.objects.select_related('user').filter(user=user).all()
            point = user.pointhistory_set.all().order_by('-created_at')

            page = self.paginate_queryset(point)
            serializer = PointHistorySerializer(page, many=True)

            if page is not None:
                serializer = PointHistorySerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise exceptions.ValidationError({'detail': 'this post not exist'}, 400)

    def get(self, request, *args, **kwargs):
        return self.list(request)