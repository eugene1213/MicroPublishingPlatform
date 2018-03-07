from rest_framework import status, exceptions, generics
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Comment, Post
from column.pagination import CommentPagination
from column.serializers import CommentSerializer

__all__ = (
    'CommentListView',
    'CommentLikeToggleView',
    'CommentCreateView'
)


class CommentCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def post(self, request):
        post_id = self.request.data['post_id']
        content = self.request.data['content']
        post = Post.objects.filter(pk=post_id).get()
        user = self.request.user

        comment, result = Comment.objects.create(author=user, content=content, post=post)

        if result:
            return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Already added."}, status=status.HTTP_200_OK)


class CommentListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def list(self, request, *args, **kwargs):
        param = self.kwargs.get('pk')
        post = Post.objects.filter(pk=param).get()
        queryset = Comment.objects.filter(post=post, parent__isnull=True).order_by('-created_date').all()

        page = self.paginate_queryset(queryset)
        serializer = CommentSerializer(page, many=True)

        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        param = self.kwargs.get('pk')
        if param == '':
            raise exceptions.ValidationError({'detail': 'this param is wht'}, 400)

        return self.list(request)


class CommentLikeToggleView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = self.request.data
        comment_instance = get_object_or_404(Comment, pk=data['comment_id'])
        comment_like, comment_like_created = comment_instance.commentlike_set.get_or_create(
            user=request.user
        )
        if not comment_like_created:
            comment_like.delete()
        return Response({'created': comment_like_created})
