from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, exceptions, generics
from rest_framework.generics import get_object_or_404
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

    def parent(self, parent):
        if parent == '':
            return None
        return parent

    def post(self, request):
        data = self.request.data

        post_id = data['post_id']
        content = data['content']
        try:
            parent = self.parent(data['comment_id'])

            post = Post.objects.filter(pk=post_id).get()
            user = self.request.user
            parent_comment = Comment.objects.filter(pk=parent, post=post).get()
            comment = Comment.objects.create(author=user, content=content, post=post)

            if comment:
                if comment.is_parent:
                    comment.parent = parent_comment
                    comment.save()
                    return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)
                raise exceptions.ValidationError({'detail': 'this param is wht'}, 400)
            else:
                return Response({"detail": "Already added."}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            post = Post.objects.filter(pk=post_id).get()
            user = self.request.user
            comment = Comment.objects.create(author=user, content=content, post=post, parent=None)

            if comment:
                return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Already added."}, status=status.HTTP_200_OK)


class CommentListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def list(self, request, *args, **kwargs):
        param = self.kwargs.get('post_pk')

        try:
            post = Post.objects.filter(pk=param).get()
            queryset = Comment.objects.filter(post=post, parent__isnull=True).order_by('-created_date').all()

            page = self.paginate_queryset(queryset)
            serializer = CommentSerializer(page, many=True)

            if page is not None:
                serializer = CommentSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise exceptions.ValidationError({'detail': 'this post not exist'}, 400)

    def get(self, request, *args, **kwargs):
        param = self.kwargs.get('post_pk')
        if param == '':
            raise exceptions.ValidationError({'detail': 'this param is wht'}, 400)

        return self.list(request)


class CommentLikeToggleView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        param = self.kwargs.get('comment_pk')
        try:
            comment_instance = Comment.objects.filter(pk=param).get()
            result = Comment.like_toggle(user=user, comment=comment_instance)
            if result:
                return Response({'detail': 'created'})
            return Response({'created': 'deleted'})
        except ObjectDoesNotExist:
            raise exceptions.ValidationError({"detail": "Abnormal connected"})
