from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Post
from column.serializers import PostMoreSerializer

__all__ = (
    'Search',
)


class Search(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = self.request.data
        post_list = Post.objects.filter(
            Q(title__icontains=data['word']) | Q(author__nickname__icontains=data['word'])
        ).distinct()
        serailizer = PostMoreSerializer(post_list, context={'user': self.request.user}, many=True)
        return Response(serailizer.data, status=status.HTTP_200_OK)