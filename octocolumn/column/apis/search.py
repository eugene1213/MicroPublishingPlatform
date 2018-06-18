from itertools import chain
from operator import attrgetter

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Post, SearchTag
from column.pagination import PostPagination
from column.serializers import PostMoreSerializer
from utils.error_code import kr_error_code

__all__ = (
    'Search',
)


class Search(generics.ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = PostPagination

    def list(self, request, *args, **kwargs):
        try:
            data = request.GET
            if len(data['keyword']) < 2:
                return Response(
                    {
                        "code": 426,
                        "message": kr_error_code(426)
                    }
                    , status=status.HTTP_400_BAD_REQUEST
                )
            post_list = Post.objects.select_related('author').filter(
                Q(title__icontains=data['keyword']) | Q(author__nickname__icontains=data['keyword'])
            ).distinct()
            tag = SearchTag.objects.select_related('post').filter(
                Q(tag__icontains=data['keyword'])
            ).distinct()
            tag_list = []
            for i in tag:
                tag_list.append(i.post)

            all_post = sorted(chain(post_list, tag_list), key=attrgetter('created_date'), reverse=True)

            page = self.paginate_queryset(all_post)
            serializer = PostMoreSerializer(page, context={'user': self.request.user}, many=True)

            if page is not None:
                serializer = PostMoreSerializer(page, context={'user': self.request.user}, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response('', 200)

    def get(self, request, *args, **kwargs):
        return self.list(request)