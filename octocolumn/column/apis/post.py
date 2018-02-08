from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, generics, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Temp, Comment
from column.pagination import PostPagination
from member.models import Author as AuthorModel, User
from ..models import Post
from ..serializers import PostSerializer

__all__ = (
    # 'PostListCreateView',
    'PostLikeToggleView',
    'PostCreateView',
)


# 포스트를 생성하는 APIview
class PostCreateView(generics.GenericAPIView,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def is_post(self, temp_id):
        # temp = Temp.objects.filter(id=temp_id)
        # if temp.author_id != self.request.user.id:
        #   return False
        # return True
        pass

    def decrease_point(self):
        return User.objects.filter(user=self.request.user).update(point=self.request.user.point-300)

    def is_author(self):
        try:
            author = AuthorModel.objects.all().get(author_id=self.request.user.id)
            return author
        except ObjectDoesNotExist:
            author = None
            return author

    # if is_post(data['temp_id']):
    #   raise exceptions.ParseError({"detail":"You are not the owner of this article"})

    def post(self, request):
        user = self.request.user
        data = self.request.data

        # 1. 작가가 신청되어있는지 확인
        # 2. 작가 활성이 되어있는지를 확인
        author = self.is_author()

        if author is not None:
            if author.is_active:
                return Response({"detail": "This Account is Deactive"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "This Account is not Author"}, status=status.HTTP_200_OK)

        temp = Temp.objects.filter(id=data['id']).get()

        if 300 > user.point:
            raise Response({"detail": "There is not enough points."} , status=status.HTTP_400_BAD_REQUEST)

        post, result = super().get_queryset().get_or_create(author=user, title=temp.title,
                                                            main_content=temp.main_content,
                                                            price=data['price']
                                                            )

        # if is_post(data['temp_id']):
        #   raise exceptions.ParseError({"detail":"You are not the owner of this article"})

        Temp.objects.delete(id=data['id'])

        self.decrease_point()

        if result:
            return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Already added."}, status=status.HTTP_200_OK)


#
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def perform_create(self, serializer):
        # serializer.save()로 생성된 Post instance를 instance변수에 할당
        instance = serializer.save(author=self.request.user)
        # comment_content에 request.data의 'comment'에 해당하는 값을 할당
        comment_content = self.request.data.get('comment')
        # 'comment'에 값이 왔을 경우, my_comment항목을 채워줌
        if comment_content:
            instance.my_comment = Comment.objects.create(
                post=instance,
                author=instance.author,
                content=comment_content
            )
            instance.save()


class PostLikeToggleView(APIView):
    def post(self, request, post_pk):
        post_instance = get_object_or_404(Post, pk=post_pk)
        post_like, post_like_created = post_instance.postlike_set.get_or_create(
            user=request.user
        )
        if not post_like_created:
            post_like.delete()
        return Response({'created': post_like_created})


