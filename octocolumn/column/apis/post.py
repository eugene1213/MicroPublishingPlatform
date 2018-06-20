import base64
import operator
import re

from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from rest_framework import status, generics, mixins, exceptions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Temp, SearchTag, PostStar, Tag, Recommend
from column.pagination import PostPagination, PostListPagination
from column.serializers.tag import SearchTagSerializer
from member.models import Author as AuthorModel, User, PointHistory, BuyList, ProfileImage, Profile
from member.models.user import WaitingRelation, Bookmark, Relation
from member.serializers import ProfileImageSerializer, UserSerializer
from octo.models import UsePoint
from utils.error_code import kr_error_code
from utils.image_rescale import image_quality_down, thumnail_cover_image_resize
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
    'BookmarkListView',
    'BuyListView',
    'FeedListView'
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
    def search_tag(self, post, tag):
        search_tag = tag.split(',')
        if len(search_tag) > 5:
            return Response(
                {
                    "code": 413,
                    "message": kr_error_code(413)
                }
                , status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        for i in search_tag:
            tags = Tag.objects.create(tags=i)
            post.tags.add(tags)

        return True

    def recommend_text(self, post, recommend):
        recommend_tag = recommend.split('|')

        if len(recommend_tag) > 5:
            return Response(
                {
                    "code": 413,
                    "message": kr_error_code(413)
                }
                , status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        for i in recommend_tag:
            tags = Recommend.objects.create(text=i)
            post.recommand.add(tags)

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
        return Response(
            {
                "code": 412,
                "message": kr_error_code(412)
            }
            , status=status.HTTP_412_PRECONDITION_FAILED)

    def post(self, request):
        user = self.request.user
        data = self.request.data

        cover_file_obj = self.base64_content(self.request.data['cover'])
        resizing_image = image_quality_down(cover_file_obj)
        thumbnail_image = thumnail_cover_image_resize(cover_file_obj)

        # 1. 작가가 신청되어있는지 확인
        # 2. 작가 활성이 되어있는지를 확인

        author = self.is_author()
        # 작가 일 경우
        if author is not None:
            # 작가가 활성화 되지 않았을경우
            if author.is_active:
                # 임시저장 파일이 없을 경우
                if data['temp_id'] == '':
                    return Response(
                        {
                            "code": 500,
                            "message": kr_error_code(500)
                        }
                        , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                try:
                    temp = Temp.objects.filter(id=data['temp_id']).get()
                except ObjectDoesNotExist:
                    return Response(
                        {
                            "code": 409,
                            "message": kr_error_code(409)
                        }
                        , status=status.HTTP_409_CONFLICT)

                # 포인트가 모자르다면 에러발생
                # 정확한 정보를 위해 db의 유저 정보를 가져온다

                # if self.is_post(data['temp_id']):
                #     raise exceptions.ParseError({"detail": "You are not the owner of this article"})

                post = Post.objects.create(author=user, title=temp.title,
                                           main_content=temp.main_content,
                                           price=data['price'],
                                           cover_image=resizing_image,
                                           thumbnail=thumbnail_image,
                                           preview=data['preview']
                                           )
                PostStar.objects.create(post=post)

                serializer = PostSerializer(post)
                # 태그 추가
                if data['tag'] != '':
                    if not self.search_tag(post, data['tag']):
                        return Response(
                            {
                                "code": 413,
                                "message": kr_error_code(413)
                            }
                            , status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

                if data['recommend'] != '':
                    if not self.recommend_text(post, data['recommend']):
                        return Response(
                            {
                                "code": 413,
                                "message": kr_error_code(413)
                            }
                            , status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

                # 유저 포인트 업데이트
                self.waiting_init()
                self.add_point_history(point=0, post=post, history=temp.title)

                # 템프파일 삭제
                try:
                    Temp.objects.filter(id=data['temp_id']).delete()
                except ObjectDoesNotExist:
                    return Response(
                        {
                            "code": 409,
                            "message": kr_error_code(409)
                        }
                        , status=status.HTTP_409_CONFLICT)

                # 태그를 추가하고 태그 추가 실패

                if serializer:
                    return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        {
                            "code": 408,
                            "message": kr_error_code(408)
                        }
                        , status=status.HTTP_408_REQUEST_TIMEOUT)
            else:
                return Response(
                    {
                        "code": 405,
                        "message": kr_error_code(405)
                    }
                    , status=status.HTTP_405_METHOD_NOT_ALLOWED)

        else:
            return Response(
                {
                    "code": 500,
                    "message": kr_error_code(500)
                }
                , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


################################### 목록  ###############################

class PostListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = PostListPagination
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            post = Post.objects.select_related('author').all().order_by('-created_date')[0:10]

            page = self.paginate_queryset(post)
            serializer = PostMoreSerializer(page, context={'user': self.request.user}, many=True)

            if page is not None:
                serializer = PostMoreSerializer(page, context={'user': self.request.user}, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response('', 200)

    def get(self, request, *args, **kwargs):
        return self.list(request)


class PostMoreListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = PostListPagination
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        try:
            post = Post.objects.all().order_by('-created_date')

            page = self.paginate_queryset(post)
            serializer = PostMoreSerializer(page, context={'user': self.request.user}, many=True)

            if page is not None:
                serializer = PostMoreSerializer(page, context={'user': self.request.user}, many=True)
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
    permission_classes = (AllowAny,)

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
            return Response(
                {
                    "code": 409,
                    "message": kr_error_code(409)
                }
                , status=status.HTTP_409_CONFLICT)
        return Post.objects.select_related('author').filter(pk=post_id).get()

    def bookmark_status(self, post):
        user = self.request.user
        if user.is_authenticated:
            try:
                Bookmark.objects.select_related('user').filter(user=self.request.user, post=post).get()
                return True
            except ObjectDoesNotExist:
                return False
        else:
            return False

    def follow_status(self, author):
        user = self.request.user
        if user.is_authenticated:
            if author == user:
                return 2
            try:
                Relation.objects.select_related('to_user', 'from_user').filter(to_user=author, from_user=user).get()
                return True
            except ObjectDoesNotExist:
                return False
        return False

    def star_rating(self, post):
        try:
            star = PostStar.objects.filter(post=post).get()
            if star.member_num == 0:
                return 0
            return round(star.content / star.member_num)
        except ObjectDoesNotExist:
            star = PostStar.objects.create(post=post)
            if star.member_num == 0:
                return 0
            return round(star.content / star.member_num)

    def get(self, request, *args, **kwargs):
        param = self.kwargs.get('pk')

        post = self.post_exist(param)

        serializer = PostSerializer(post)

        user = self.request.user

        # 0 원일 경우
        if user.is_authenticated:
            # 0원이아닐경우 체크
            if self.is_buyed(post):
                # 구매했을때 원본 출력
                if serializer:
                    # 조회수 증가
                    post.hit += 1
                    post.save()
                    # 작가임
                    author = post.author
                    user_serializer = UserSerializer(author)
                    profile_image = ProfileImage.objects.select_related('user').filter(user=author).get()
                    image_serializer = ProfileImageSerializer(profile_image)
                    time = datetime.strptime(serializer.data['created_date'].split('T')[0], '%Y-%m-%d')
                    profile = Profile.objects.select_related('user').filter(user=author).get()

                    return Response({
                        "detail": {
                            "post_id": serializer.data['pk'],
                            "cover_img": serializer.data['cover_image'],
                            "main_content": serializer.data['main_content'],
                            "title": serializer.data['title'],
                            "tag": self.tag(post),
                            "bookmark_status": self.bookmark_status(post),
                            "follow_status": self.follow_status(author),
                            "following_url": "/api/member/" + str(user_serializer.data['pk'], 'utf-8') + "/follow/",
                            "star": self.star_rating(post),
                            "waiting": WaitingRelation.objects.filter(receive_user=author).count(),
                            "author": {
                                "author_id": user_serializer.data['pk'],
                                "username": user_serializer.data['nickname'],
                                "intro": profile.intro,
                                "image": image_serializer.data
                            },

                            'created_datetime': time.strftime('%Y.%m.%d'),

                        }
                    }, status=status.HTTP_200_OK)
                return Response(
                    {
                        "code": 500,
                        "message": kr_error_code(500)
                    }
                    , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(
                {
                    "code": 407,
                    "message": kr_error_code(407)
                }
                , status=status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED)

        else:
            if post.price == 0:
                if serializer:
                    # 조회수 증가
                    post.hit += 1
                    post.save()
                    # 작가임
                    author = post.author
                    user_serializer = UserSerializer(author)
                    profile_image = ProfileImage.objects.select_related('user').filter(user=author).get()
                    image_serializer = ProfileImageSerializer(profile_image)
                    time = datetime.strptime(serializer.data['created_date'].split('T')[0], '%Y-%m-%d')
                    profile = Profile.objects.select_related('user').filter(user=author).get()

                    return Response({
                        "detail": {
                            "post_id": serializer.data['pk'],
                            "cover_img": serializer.data['cover_image'],
                            "main_content": serializer.data['main_content'],
                            "title": serializer.data['title'],
                            "tag": self.tag(post),
                            "bookmark_status": self.bookmark_status(post),
                            "follow_status": self.follow_status(author),
                            "following_url": "/api/member/" + str(user_serializer.data['pk'], 'utf-8') + "/follow/",
                            "star": self.star_rating(post),
                            "waiting": WaitingRelation.objects.filter(receive_user=author).count(),
                            "author": {
                                "author_id": author.pk,
                                "username": author.nickname,
                                "intro": profile.intro,
                                "image": image_serializer.data
                            },

                            'created_datetime': time.strftime('%Y.%m.%d'),

                        }
                    }, status=status.HTTP_200_OK)


class PostPreReadView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        param = self.kwargs.get('pk')
        post = Post.objects.filter(pk=param).get()
        serializer = PostSerializer(post)

        if serializer:
            return Response(serializer.data['preview_image'], status=status.HTTP_200_OK)
        return Response(
            {
                "code": 500,
                "message": kr_error_code(500)
            }
            , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IsBuyPost(APIView):
    permission_classes = (AllowAny,)

    def main_content(self, obj):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', obj)
        return clean_text[:300]

    def tag(self, post):
        tag = SearchTag.objects.filter(post=post)
        tag_serializer = SearchTagSerializer(tag, many=True)
        if tag_serializer:
            return tag_serializer.data
        return None

    def except_division(self, star):
        try:
            return round(star.content / star.member_num)
        except ZeroDivisionError:
            return 0

    def get(self, request, *args, **kwargs):
        param = self.kwargs.get('pk')
        user = self.request.user
        if user.is_authenticated:
            try:
                post = Post.objects.filter(id=param).get()
                star = PostStar.objects.filter(post=post).get()
                serializer = PostSerializer(post)
                try:
                    BuyList.objects.filter(user=user, post=post).get()
                    return Response({"detail": {
                        "isBuy": True,
                        "title": serializer.data['title'],
                        "nickname": post.author.nickname,
                    }}, status=status.HTTP_200_OK)

                except ObjectDoesNotExist:
                    if post.author == user:
                        return Response({"detail": {
                            "isBuy": True,
                            "title": serializer.data['title'],
                            "nickname": post.author.nickname,

                        }}, status=status.HTTP_200_OK)
                    return Response({"detail": {
                        "isBuy": False,
                        "cover_image": serializer.data['cover_image'],
                        "created_datetime": post.created_date.strftime('%Y.%m.%d') + ' ' +
                                            post.created_date.strftime('%H:%M'),
                        "price": serializer.data['price'],
                        "preview": serializer.data['preview'],
                        "title": serializer.data['title'],
                        "nickname": post.author.nickname,
                        "main_content": self.main_content(post.main_content),
                        "tag": self.tag(post),
                        "star": self.except_division(star),
                        "point": '보유 포인트: ' + str(user.point) +'P'


                    }},
                        status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                raise exceptions.NotFound()

        else:
            try:
                post = Post.objects.filter(id=param).get()
                star = PostStar.objects.filter(post=post).get()
                if star:
                    pass
                else:
                    star = PostStar.objects.create(post=post)

                serializer = PostSerializer(post)

                if post.price == 0:
                    return Response({"detail": {
                        "isBuy": True,
                        "title": serializer.data['title'],
                        "nickname": post.author.nickname,
                    }}, status=status.HTTP_200_OK)

                return Response({"detail": {
                    "isBuy": False,
                    "cover_image": serializer.data['cover_image'],
                    "created_datetime": post.created_date.strftime('%Y.%m.%d') + ' ' + post.created_date.strftime(
                        '%H:%M'),
                    "price": serializer.data['price'],
                    "preview": serializer.data['preview'],
                    "title": serializer.data['title'],
                    "nickname": post.author.nickname,
                    "main_content": self.main_content(post.main_content),
                    "tag": self.tag(post),
                    "star": self.except_division(star),
                    "point": '로그인 해주세요'

                }},
                    status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                return Response(
                    {
                        "code": 404,
                        "message": kr_error_code(404)
                    }
                    , status=status.HTTP_404_NOT_FOUND)


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


# 1
# 북마크 리스트 API
# /api/column/bookmarkList/
class BookmarkListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PostPagination
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        list = []
        try:
            post = User.objects.filter(pk=self.request.user.id).get().bookmark_user_relation.all()
            for i in post:
                list.append(i.post)

            page = self.paginate_queryset(list)
            serializer = PostMoreSerializer(page, context={'user': self.request.user}, many=True)

            if page is not None:
                serializer = PostMoreSerializer(page, context={'user': self.request.user}, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response('', 200)

    def get(self, request, *args, **kwargs):
        return self.list(request)


# 구매목록 최신순
class BuyListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PostPagination
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        list = []
        try:
            post = BuyList.objects.select_related('user', 'post').filter(user=user).all().order_by('-created_at')
            for i in post:
                list.append(i.post)

            page = self.paginate_queryset(list)
            serializer = PostMoreSerializer(page, context={'user': self.request.user}, many=True)

            if page is not None:
                serializer = PostMoreSerializer(page, context={'user': self.request.user}, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response('', 200)

    def get(self, request, *args, **kwargs):
        return self.list(request)


class FeedListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PostPagination
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        list = []
        try:
            follower = Relation.objects.select_related('to_user', 'from_user').filter(from_user=user).all()
            for i in follower:
                post = Post.objects.select_related('author').filter(author=i.to_user).all()
                for j in post:
                    list.append(j)

            list.sort(key=operator.attrgetter('created_date'))
            page = self.paginate_queryset(list)
            serializer = PostMoreSerializer(page, context={'user': self.request.user}, many=True)

            if page is not None:
                serializer = PostMoreSerializer(page, context={'user': self.request.user}, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response('', 200)

    def get(self, request, *args, **kwargs):
        return self.list(request)
