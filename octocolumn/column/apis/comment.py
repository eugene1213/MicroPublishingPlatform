from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Comment, Post
from column.pagination import CommentPagination
from column.serializers import CommentSerializer
from member.models import Notification
from utils.error_code import kr_error_code

__all__ = (
    'CommentListView',
    'CommentLikeToggleView',
    'CommentView'
)


class CommentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def comment_notify(self, user, comment):
        notify = Notification.objects.create(comment=comment)

        user.notify.add(notify)
        return True

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

            post = Post.objects.select_related('author').filter(pk=post_id).get()
            user = self.request.user
            parent_comment = Comment.objects.select_related('author', 'post').filter(pk=parent, post=post).get()
            comment = Comment.objects.create(author=user, content=content, post=post)

            if comment:
                self.comment_notify(parent_comment.author, comment)
                if comment.is_parent:
                    comment.parent = parent_comment
                    comment.save()
                    return Response({"detail": comment.pk}, status=status.HTTP_201_CREATED)
                return Response(
                    {
                        "code": 422,
                        "message": kr_error_code(422)
                    }
                    , status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response({"detail": "Already added."}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            post = Post.objects.filter(pk=post_id).get()
            user = self.request.user
            comment = Comment.objects.create(author=user, content=content, post=post, parent=None)

            if comment:
                self.comment_notify(post.author, comment)
                return Response({"detail": comment.pk}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Already added."}, status=status.HTTP_200_OK)

    def put(self, request):
        user = self.request.user
        data = self.request.data
        try:
            comment = Comment.objects.select_related('author', 'post').filter(pk=data['comment_id']).get()

            if comment.author == user:
                if not comment.is_deleted:
                    comment.content = data['content']
                    comment.save()
                    return Response({"detail": "success"}, status=status.HTTP_200_OK)
                return Response(
                    {
                        "code": 423,
                        "message": kr_error_code(423)
                    }
                    , status=status.HTTP_423_LOCKED)
            return Response(
                {
                    "code": 402,
                    "message": kr_error_code(402)
                }
                , status=status.HTTP_402_PAYMENT_REQUIRED)
        except ObjectDoesNotExist:
            return Response(
                {
                    "code": 500,
                    "message": kr_error_code(500)
                }
                , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        user = self.request.user
        data = self.request.data
        try:
            comment = Comment.objects.select_related('author', 'post').filter(pk=data['comment_id']).get()

            if comment.author == user:
                if comment.children().count() is not 0:

                    comment.is_deleted = True
                    comment.content = "삭제된 댓글입니다."
                    comment.save()
                    return Response({"detail": "success"}, status=status.HTTP_200_OK)
                comment.delete()
                return Response({"detail": "deleted"}, status=status.HTTP_204_NO_CONTENT)
            return Response(
                {
                    "code": 402,
                    "message": kr_error_code(402)
                }
                , status=status.HTTP_402_PAYMENT_REQUIRED)
        except ObjectDoesNotExist:
            return Response(
                {
                    "code": 500,
                    "message": kr_error_code(500)
                }
                , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def list(self, request, *args, **kwargs):
        post_pk = self.kwargs.get('post_pk')
        comment_id = self.kwargs.get('comment_id')

        if comment_id is None:
            try:
                post = Post.objects.select_related('author').filter(pk=post_pk).get()
                queryset = Comment.objects.select_related('author', 'post').filter(post=post, parent__isnull=True).order_by('-created_date').all()

                page = self.paginate_queryset(queryset)
                serializer = CommentSerializer(page, context={'request': request}, many=True)

                if page is not None:
                    serializer = CommentSerializer(page, context={'request': request},  many=True)
                    return self.get_paginated_response(serializer.data)

                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response(
                    {
                        "code": 409,
                        "message": kr_error_code(409)
                    }
                    , status=status.HTTP_409_CONFLICT)

        else:
            try:
                post = Post.objects.filter(pk=post_pk).get()
                try:
                    parent = Comment.objects.select_related('parent').filter(pk=comment_id).get()
                    queryset = Comment.objects.select_related('post','parent').filter(post=post, parent=parent).order_by('-created_date').all()

                    page = self.paginate_queryset(queryset)
                    serializer = CommentSerializer(page, context={'request': request}, many=True)

                    if page is not None:
                        serializer = CommentSerializer(page, context={'request': request}, many=True)
                        return self.get_paginated_response(serializer.data)

                    return Response(serializer.data)
                
                except ObjectDoesNotExist:
                    return Response(
                        {
                            "code": 423,
                            "message": kr_error_code(423)
                        }
                        , status=status.HTTP_423_LOCKED)

            except ObjectDoesNotExist:
                return Response(
                    {
                        "code": 409,
                        "message": kr_error_code(409)
                    }
                    , status=status.HTTP_409_CONFLICT)

    def get(self, request, *args, **kwargs):
        param = self.kwargs.get('post_pk')
        if param == '':
            return Response(
                {
                    "code": 422,
                    "message": kr_error_code(422)
                }
                , status=status.HTTP_422_UNPROCESSABLE_ENTITY)

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
            return Response(
                {
                    "code": 500,
                    "message": kr_error_code(500)
                }
                , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


