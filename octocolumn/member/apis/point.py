from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from member.models import PointHistory
from member.pagination import PointHistoryPagination
from member.serializers.point import PointHistorySerializer


class UserPointHistory(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PointHistoryPagination

    def list(self, request, *args, **kwargs):
        try:
            point = PointHistory.objects.filter(user=self.request.user)

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