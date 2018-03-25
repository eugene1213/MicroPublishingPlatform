import base64
import re

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from rest_framework import status, generics, mixins, exceptions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Temp, SearchTag
from column.pagination import PostPagination
from column.serializers.tag import SearchTagSerializer
from member.models import Author as AuthorModel, User, PointHistory, BuyList, ProfileImage
from member.models.user import Relation, WaitingRelation, Bookmark
from member.serializers import ProfileImageSerializer
from octo.models import UsePoint
from ..models import Post
from ..serializers import PostSerializer, PostMoreSerializer

__all__ = (
    'PostLikeToggleView',
    'PostCreateView',
    'PostReadView',
    'PostPreReadView',
    'AuthorResult',
    'IsBuyPost',
    'PostListView',
    'PostMoreListView',
    'BookmarkListView'
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
        temp = Temp.objects.filter(id=temp_id).get()
        if temp.author == self.request.user:
            return True
        return False

    def validate_code(self, code):
        pass

    # 포인트 감소
    def decrease_point(self, point):
        return User.objects.filter(id=self.request.user.id).update(point=point)

    # 작가인증
    def is_author(self):
        try:
            author = AuthorModel.objects.filter(author=self.request.user).get()
            return author
        except ObjectDoesNotExist:
            author = None
            return author

    # 포인트사용내역에 추가
    def add_point_history(self, point, post, history):
        return PointHistory.objects.publish(user=self.request.user, point=point, post=post,
                                            history=history)

    # 검색 태그 추가
    def search_tag(self, post_id, tag):
        search_tag = tag.split(',')
        if len(search_tag) > 5:
            raise exceptions.ValidationError({'detail': 'You can`t add up to 5'}, 200)

        for i in search_tag:
            SearchTag.objects.create(post_id=post_id, tag=i)

        return True

    def major_point(self):
        return UsePoint.objects.filter(type='major_user').get()

    def first_point(self):
        return UsePoint.objects.filter(type='first_user').get()

    def waiting_init(self):
        # 웨이팅 릴레이션 모두 삭제
        if WaitingRelation.objects.filter(receive_user=self.request.user).all().delete():
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

    def post(self, request):
        user = self.request.user
        data = self.request.data

        cover_file_obj = self.base64_content(self.request.data['cover'])

        # 1. 작가가 신청되어있는지 확인
        # 2. 작가 활성이 되어있는지를 확인

        author = self.is_author()
        # 작가 일 경우
        if author is not None:
            # 작가가 활성화 되지 않았을경우
            if author.is_active:
                # 임시저장 파일이 없을 경우
                if data['temp_id'] == '':
                    raise exceptions.NotAcceptable({'detail': 'Abnormal connected'}, 400)
                try:
                    temp = Temp.objects.filter(id=data['temp_id']).get()
                except ObjectDoesNotExist:
                    raise exceptions.NotAcceptable({'detail': 'Already Posted or temp not exist'}, 400)

                # 포인트가 모자르다면 에러발생
                # 정확한 정보를 위해 db의 유저 정보를 가져온다
                user_queryset = User.objects.filter(id=self.request.user.id).get()

                # if self.is_post(data['temp_id']):
                #     raise exceptions.ParseError({"detail": "You are not the owner of this article"})

                if self.major_point().point > user_queryset.point:
                    raise exceptions.NotAcceptable({"detail": "There is not enough points."}, 400)

                post = Post.objects.create(author=user, title=temp.title,
                                           main_content=temp.main_content,
                                           price=data['price'],
                                           cover_image=cover_file_obj
                                           )
                serializer = PostSerializer(post)
                # 태그 추가
                if data['tag'] != '':
                    if not self.search_tag(post_id=serializer.data['pk'], tag=self.request.data['tag']):
                        raise exceptions.ValidationError({'detail': 'Upload tag Failed'}, 400)

                # 유저 포인트 업데이트
                user_queryset.point -= self.major_point().point
                user_queryset.save()
                self.waiting_init()
                self.add_point_history(point=self.major_point().point, post=post, history=temp.title)

                # 템프파일 삭제
                try:
                    Temp.objects.filter(id=data['temp_id']).delete()
                except ObjectDoesNotExist:
                    raise exceptions.ValidationError({'detail': 'Already Posted or temp not exist'}, 400)

                # 태그를 추가하고 태그 추가 실패

                if serializer:
                    return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)
                else:
                    raise exceptions.ValidationError({'detail': 'Already added'}, 400)
            else:
                raise exceptions.NotAcceptable({"detail": "This Account is Deactive "}, 401)

        else:
            raise exceptions.ValidationError({"detail": "Abnormal connected"})


class PostListView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def remove_tag(self, post):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', post)
        return clean_text

    # 태그 처리 함수
    def tag(self, post):
        tag = SearchTag.objects.filter(post=post)
        tag_serializer = SearchTagSerializer(tag, many=True)
        if tag_serializer:
            return tag_serializer.data
        return None

    def image(self, user):
        try:
            img = ProfileImage.objects.filter(user=user).get()

            return ProfileImageSerializer(img).data
        except ObjectDoesNotExist:
            return {
                "profile_image": 'example/2_x20_.jpeg',
                "cover_image": 'example/1.jpeg'
                    }

    def follower_status(self, user):
        if self.request.auth is None:
            return False
        try:
            Relation.objects.filter(to_user=user, from_user=self.request.user).get()
            return True
        except ObjectDoesNotExist:
            return False

    def get(self, request, *args, **kwargs):
        post = Post.objects.order_by('-created_date')[:5]

        lists = []
        for i in post:
            content = i.main_content
            rm_content = self.remove_tag(content)[0:1000]
            user = User.objects.filter(pk=i.author_id).get()

            serializer = PostSerializer(i)
            time = datetime.strptime(serializer.data['created_date'].split('T')[0], '%Y-%m-%d')
            time2 = datetime.strptime(serializer.data['created_date'].split('T')[1].split('.')[0], '%H:%M:%S')
            text = self.remove_tag(content)
            follower_count = Relation.objects.filter(to_user=user).count()
            tag = self.tag(i)

            data = {
                "post": {
                    "post_id": serializer.data['pk'],
                    "title": serializer.data['title'],
                    "main_content": rm_content,
                    "cover_img": serializer.data['cover_image'],
                    "created_date": time.strftime('%B')[:3] + time.strftime(' %d'),
                    'created_datetime': time.strftime('%Y.%m.%d') + ' ' + time2.strftime('%H:%M'),
                    "typo_count": len(text) - text.count(' ') / 2,
                    "tag": tag,
                    "price": serializer.data['price'],
                    "author": {
                        "author_id": serializer.data['author'],
                        "username": user.nickname,
                        "follow_status": self.follower_status(user),
                        "follower_count": follower_count,
                        "following_url": "/api/member/" + str(user.pk) + "/follow/",
                        "achevement": "",
                        "img": self.image(user)

                    }
                }
            }
            lists.append(data)

        return Response(lists, status=status.HTTP_200_OK)


class PostMoreListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = PostPagination
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        try:
            post = Post.objects.all().order_by('-created_date')

            page = self.paginate_queryset(post)
            serializer = PostMoreSerializer(page, context={'request': request}, many=True)

            if page is not None:
                serializer = PostMoreSerializer(page, context={'request': request}, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response('', 200)

    def get(self, request, *args, **kwargs):
        return self.list(request)


class f(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PostPagination
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        try:
            user = self.request.user
            post = Bookmark.objects.filter(user=user).order_by('-created_date')

            page = self.paginate_queryset(post)
            serializer = PostMoreSerializer(page, context={'request': request}, many=True)

            if page is not None:
                serializer = PostMoreSerializer(page, context={'request': request}, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response('', 200)

    def get(self, request, *args, **kwargs):
        return self.list(request)


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

    def is_buyed(self, post):
        try:
            BuyList.objects.filter(user=self.request.user, post=post).get()
            return True
        except ObjectDoesNotExist:
            if self.request.user == post.author:
                return True
            return False

    def tag(self, post):
        tag = SearchTag.objects.filter(post=post)
        tag_serializer = SearchTagSerializer(tag, many=True)
        if tag_serializer:
            return tag_serializer.data
        return None

    def post_exist(self, post_id):
        if Post.objects.filter(pk=post_id).count() == 0:
            raise exceptions.ValidationError({'detail': 'Does not exist post'}, 400)
        return Post.objects.filter(pk=post_id).get()

    def get(self, request, *args, **kwargs):
        param = self.kwargs.get('pk')

        post = self.post_exist(param)

        serializer = PostSerializer(post)

        # 구매를 했는지를 검사
        if self.is_buyed(post):
            # 구매했을때 원본 출력
            if serializer:
                # 조회수 증가
                post.hit += 1
                post.save()
                # 작가임
                user = User.objects.filter(pk=post.author_id).get()
                profile_image = ProfileImage.objects.filter(user=user).get()
                image_serializer = ProfileImageSerializer(profile_image)
                time = datetime.strptime(serializer.data['created_date'].split('T')[0], '%Y-%m-%d')
                SearchTagSerializer()
                return Response({
                    "detail": {
                        "post_id": serializer.data['pk'],
                        "cover_img": serializer.data['cover_image'],
                        "main_content": serializer.data['main_content'],
                        "title": serializer.data['title'],
                        "tag": self.tag(post),
                        "author": {
                            "author_id": serializer.data['author'],
                            "username": user.nickname,
                            "achevement": "",
                            "image":image_serializer
                        },

                        'created_datetime': time.strftime('%Y.%m.%d'),

                    }
                }, status=status.HTTP_200_OK)
            raise exceptions.ValidationError({'detail': 'expected error'}, 400)
        raise exceptions.ValidationError({'detail': False}, 400)


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
            BuyList.objects.filter(user=self.request.user, post=param).get()
            return Response({"detail": {
                "isBuy": True
            }}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            post = Post.objects.filter(pk=param).get()
            serializer = PostSerializer(post)

            if serializer:
                return Response({"detail": {
                    "isBuy": False,
                    "preview": serializer.data['preview_image'],
                }},
                    status=status.HTTP_200_OK)
            raise exceptions.ValidationError({'detail': 'expected error'}, 400)


class AuthorResult(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            author = AuthorModel.objects.filter(author=self.request.user).get()
            if author is not None:
                if author.is_active:
                    return Response({"author": True}, status=status.HTTP_200_OK)
                return Response({"author": False}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"author": False}, status=status.HTTP_200_OK)


class BookmarkListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PostPagination
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        try:
            user = self.request.user
            post = Bookmark.objects.filter(user=user).order_by('-created_date')

            page = self.paginate_queryset(post)
            serializer = PostMoreSerializer(page, context={'request': request}, many=True)

            if page is not None:
                serializer = PostMoreSerializer(page, context={'request': request}, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response('', 200)

    def get(self, request, *args, **kwargs):
        return self.list(request)
