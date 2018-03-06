from rest_framework import status, exceptions
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Comment, Post
from column.serializers import CommentSerializer
from member.models import User

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


class CommentListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        param = self.kwargs.get('pk')
        post = Post.objects.filter(pk=param).get()
        comment = Comment.objects.filter(post=post, parent__isnull=True).order_by('-created_date')[:5]
        serializer = CommentSerializer(comment, many=True)

        list = []
        if serializer:
            # for i in serializer.data:
            # author_id = serializer.data['author']
            # user = User.objects.filter(pk=author_id).get()
            # data = {
            #     "comment":{
            #         "comment_id": serializer.data['pk'],
            #         "username": user.last_name + " " + user.first_name,
            #         "comment_content": serializer.data['content'],
            #     }
            # }
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise exceptions.ValidationError({'detail': ''}, 400)


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
