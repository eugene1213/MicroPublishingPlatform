import base64
import re

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from rest_framework import status, generics, mixins, exceptions
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Temp, SearchTag
from column.pagination import PostPagination
from member.models import Author as AuthorModel, User, PointHistory, BuyList
from ..models import Post
from ..serializers import PostSerializer

__all__ = (
    # 'PostListCreateView',
    'PostLikeToggleView',
    'PostCreateView',
    'PostView'
)


# 포스트를 생성하는 APIview
class PostCreateView(generics.GenericAPIView,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)

    def is_post(self, temp_id):
        # temp = Temp.objects.filter(id=temp_id)
        # if temp.author_id != self.request.user.id:
        #   return False
        # return True
        pass

    def validate_code(self,  code):
        pass

    # 포인트 감소
    def decrease_point(self, point):
        return User.objects.filter(id=self.request.user.id).update(point=point)

    # 작가인증
    def is_author(self):
        try:
            author = AuthorModel.objects.all().get(author_id=self.request.user.id)
            return author
        except ObjectDoesNotExist:
            author = None
            return author

    # 포인트사용내역에 추가
    def add_point_history(self,point,history):
        return PointHistory.objects.publish(user=self.request.user, point=point,
                                 history=history)

    # 검색 태그 추가
    def search_tag(self, post_id, tag):
        search_tag = tag.split(',')
        if search_tag.count() > 5:
            raise exceptions.ValidationError({'detail': 'You can add up to 5'}, 200)

        for i in search_tag:
            SearchTag.objects.create(post_id=post_id, tag=i)
            return True
        return False

    # base64 파일 파일 형태로
    def base64_content(self, image):
        if image is not '':
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            return data
        raise exceptions.ValidationError({'detail': 'eEmpty image'}, 400)

    # if is_post(data['temp_id']):
    #   raise exceptions.ParseError({"detail":"You are not the owner of this article"})

    def post(self, request):
        user = self.request.user
        data = self.request.data

        preview_file_obj = self.base64_content(self.request.data['preview'])
        cover_file_obj = self.base64_content(self.request.data['cover'])

        # 1. 작가가 신청되어있는지 확인
        # 2. 작가 활성이 되어있는지를 확인

        author = self.is_author()
        if author is not None:
            if not author.is_active:
                raise exceptions.NotAcceptable({"detail": "This Account is Deactive"}, 401)
        else:
            raise exceptions.NotAcceptable({"detail": "This Account is not Author"}, 401)
        # 템프파일이 삭제 되었을경우 에러 발생 예외처리
        try:
            temp = Temp.objects.filter(id=data['temp_id']).get()
        except ObjectDoesNotExist:
            raise exceptions.NotAcceptable({'detail': 'Already Posted or temp not exist'}, 400)
        # 포인트가 모자르다면 에러발생
        if 300 > user.point:
            raise exceptions.NotAcceptable({"detail": "There is not enough points."}, 400)

        serializer = PostSerializer(Post.objects.create(author=user, title=temp.title,
                                                        main_content=temp.main_content,
                                                        price=data['price'],
                                                        preview_image=preview_file_obj,
                                                        cover_image=cover_file_obj
                                                        ))
        # 템프파일 삭제

        try:
            Temp.objects.filter(id=data['temp_id']).delete()
        except ObjectDoesNotExist:
            raise exceptions.ValidationError({'detail': 'Already Posted or temp not exist'}, 400)

        user_queryset = User.objects.filter(id=self.request.user.id).get()

        self.decrease_point(user_queryset.point - 300)
        self.add_point_history(point=300, history=temp.title)
        # 태그를 추가하고 태그 추가 실패
        if not self.search_tag(post_id=serializer.data['pk'], tag=self.request.data['tag']):
            raise exceptions.ValidationError({'detail': 'Upload tag Failed'}, 400)

        if serializer:
            return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)
        else:
            raise exceptions.ValidationError({'detail': 'Already added'}, 400)


class PostListView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def remove_tag(self, post):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', post)
        return clean_text

    def get(self, request, *args, **kwargs):
        post = Post.objects.order_by('-created_date')[:15]

        lists = []
        for i in post:
            content = i.main_content
            rm_content = self.remove_tag(content)[0:1000]
            user = User.objects.filter(pk=i.author_id).get()
            # profile_img = ProfileImage.objects.filter(id=i.author_id).get()
            serializer = PostSerializer(i)
            time =datetime.strptime(serializer.data['created_date'].split('T')[0], '%Y-%m-%d')
            text = self.remove_tag(content)
            data = {
                "post":{
                    "post_id":serializer.data['id'],
                    "title": serializer.data['title'],
                    "main_content": rm_content,
                    "cover_img": serializer.data['cover_image'],
                    "created_date": time.strftime('%B')[:3] + time.strftime(' %d'),
                    "typo_count": len(text) - text.count(' ')/2,
                    "author": {
                        "author_id": serializer.data['author'],
                        "username": user.last_name + " " + user.first_name,
                        "achevement": "",
                        "profile_img": "",
                        "cover_img": ""

                    }
                }
            }
            lists.append(data)

        return Response(lists, status=status.HTTP_200_OK)


class PostLikeToggleView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_pk):
        post_instance = get_object_or_404(Post, pk=post_pk)
        post_like, post_like_created = post_instance.postlike_set.get_or_create(
            user=request.user
        )
        if not post_like_created:
            post_like.delete()
        return Response({'created': post_like_created})


class PostView(APIView):
    permission_classes = (AllowAny,)

    def is_buyed(self, post_id):
        try:
            BuyList.objects.filter(user=self.request.user, post_id=post_id).get()
            return False
        except ObjectDoesNotExist:
            return True

    def post(self, request):
        data = self.request.data

        if not self.is_buyed(data['post_id']):
            # 구매했을때 원본 출력
            return Response("원본")

        # 구매하지 않았을때 프리뷰 페이지 출려
        return Response("프리뷰")