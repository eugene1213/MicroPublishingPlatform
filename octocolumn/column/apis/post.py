import base64
import hashlib
import re

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from rest_framework import status, generics, mixins, exceptions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Temp, SearchTag, PreAuthorPost
from member.models import Author as AuthorModel, User, PointHistory, BuyList
from ..models import Post
from ..serializers import PostSerializer, PreAuthorPostSerializer

__all__ = (
    # 'PostListCreateView',
    'PostLikeToggleView',
    'PostCreateView',
    'PostReadView',
    'PostPreReadView',
    'AuthorResult',
    'IsBuyPost',
    'PostListView'
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
            if author.is_active:
                if data['temp_id'] == '':
                    raise exceptions.NotAcceptable({'detail': 'Abnormal connected'}, 400)

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
                # if not self.search_tag(post_id=serializer.data['pk'], tag=self.request.data['tag']):
                #     raise exceptions.ValidationError({'detail': 'Upload tag Failed'}, 400)

                if serializer:
                    return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)
                else:
                    raise exceptions.ValidationError({'detail': 'Already added'}, 400)
            else:
                raise exceptions.NotAcceptable({"detail": "This Account is Deactive"}, 401)

        else:
            if data['temp_id'] == '':
                raise exceptions.NotAcceptable({'detail': 'Abnormal connected'}, 400)

            try:
                temp = Temp.objects.filter(id=data['temp_id']).get()
            except ObjectDoesNotExist:
                raise exceptions.NotAcceptable({'detail': 'Already Posted or temp not exist'}, 400)
            # 포인트가 모자르다면 에러발생
            if 300 > user.point:
                raise exceptions.NotAcceptable({"detail": "There is not enough points."}, 400)

            serializer = PreAuthorPostSerializer(PreAuthorPost.objects.create(author=user, title=temp.title,
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
            # if not self.search_tag(post_id=serializer.data['pk'], tag=self.request.data['tag']):
            #     raise exceptions.ValidationError({'detail': 'Upload tag Failed'}, 400)

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
        post = Post.objects.order_by('-created_date')[:5]

        lists = []
        for i in post:
            content = i.main_content
            rm_content = self.remove_tag(content)[0:1000]
            user = User.objects.filter(pk=i.author_id).get()
            # profile_img = ProfileImage.objects.filter(id=i.author_id).get()
            serializer = PostSerializer(i)
            time =datetime.strptime(serializer.data['created_date'].split('T')[0], '%Y-%m-%d')
            text = self.remove_tag(content)
            to_user = User.objects.filter(pk=serializer.data['author']).get()
            to_user.save()
            # from_user = User.objects.filter(pk=self.request.user.id).get()
            # from_user.save()
            follower_count = to_user.following_users.count()
            # status = from_user.following_user.filter(to_user=serializer.data['author'])
            data = {
                "post":{
                    "post_id": serializer.data['pk'],
                    "title": serializer.data['title'],
                    "main_content": rm_content,
                    "cover_img": serializer.data['cover_image'],
                    "created_date": time.strftime('%B')[:3] + time.strftime(' %d'),
                    "typo_count": len(text) - text.count(' ')/2,
                    "author": {
                        "author_id": serializer.data['author'],
                        "username": user.last_name + " " + user.first_name,
                        # "follow_status": status,
                        "follower_count": follower_count,
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


class PostReadView(APIView):
    permission_classes = (IsAuthenticated,)

    def is_buyed(self, post_id):
        try:
            BuyList.objects.filter(user=self.request.user, post_id=post_id).get()
            return True
        except ObjectDoesNotExist:
            return False

    def get(self, request, *args, **kwargs):
        param = self.kwargs.get('pk')

        post = Post.objects.filter(pk=param).get()
        serializer = PostSerializer(post)
        if self.is_buyed(param):
            # 구매했을때 원본 출력
            if serializer:
                return Response(serializer.data['main_content'], status=status.HTTP_200_OK)
            raise exceptions.ValidationError({'detail': 'expected error'}, 400)
        raise exceptions.ValidationError({'detail': 'You did not buy this post'}, 400)


class PostPreReadView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        param = self.kwargs.get('pk')
        post = Post.objects.filter(pk=param).get()
        serializer = PostSerializer(post)

        if serializer:
            return Response(serializer.data['preview_image'], status=status.HTTP_200_OK)
        raise exceptions.ValidationError({'detail': 'expected error'}, 400)


class IsBuyPost(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        param = self.kwargs.get('pk')
        try:
            BuyList.objects.filter(user=self.request.user, post_id=param).get()
            return Response({"detail": {
                "isBuy": True
            }}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            post = Post.objects.filter(pk=param).get()
            serializer = PostSerializer(post)

            # print(hashlib.md5(param.encode("utf")).hexdigest())
            if serializer:
                return Response({"detail": {
                    "isBuy": False,
                    "preview": serializer.data['preview_image'],
                    "cover": serializer.data['cover_image']
                }},
                                status=status.HTTP_200_OK)
            raise exceptions.ValidationError({'detail': 'expected error'}, 400)


class AuthorResult(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            author = AuthorModel.objects.all().get(author_id=self.request.user.id)
            if author is not None:
                return Response({"author": True}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"author": False}, status=status.HTTP_200_OK)
