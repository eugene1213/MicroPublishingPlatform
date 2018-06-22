import base64

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from rest_framework import generics, mixins, exceptions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from column.models import Temp, PreAuthorPost, Post, SearchTag, PreSearchTag, PreTag, PreRecommend

from column.serializers import PostSerializer, PreAuthorPostSerializer
from member.models import Author as AuthorModel, User, PointHistory
from member.serializers import AuthorSerializer
from octo.models import UsePoint
from utils.error_code import kr_error_code
from utils.image_rescale import image_quality_down, thumnail_cover_image_resize

__all__ = (
    'AuthorApply',
)


# 1
class AuthorApply(generics.GenericAPIView,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = AuthorModel.objects.all()
    serializer_class = AuthorSerializer

    # base64 파일 파일 형태로
    def base64_content(self, image):
        if image is not '':
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            return data
        return Response(
            {
                "code": 410,
                "message": kr_error_code(410)
            }
            , status=status.HTTP_410_GONE)

    def first_point(self):
        return UsePoint.objects.filter(type='first_user').get().point

    # 검색 태그 추가
    def search_tag(self, post, tag):
        search_tag = tag.split('|~%')
        if len(search_tag) > 5:
            return Response(
                {
                    "code": 413,
                    "message": kr_error_code(413)
                }
                , status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        for i in search_tag:
            tags = PreTag.objects.create(tags=i)
            post.tags.add(tags)
        return True

    def recommend_text(self, post, recommend):
        recommend_tag = recommend.split('|~%')
        if len(recommend_tag) > 3:
            return Response(
                {
                    "code": 413,
                    "message": kr_error_code(413)
                }
                , status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        for i in recommend_tag:
            tags = PreRecommend.objects.create(text=i)
            post.recommend.add(tags)
        return True

    # 작가 신청메서드
    def post(self, request):
        user = self.request.user
        data = self.request.data

        try:
            self.request.data['cover']
        except ObjectDoesNotExist:
            return Response(
                {
                    "code": 500,
                    "message": kr_error_code(500)
                }
                , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        cover_file_obj = self.base64_content(self.request.data['cover'])
        resizing_image = image_quality_down(cover_file_obj)
        thumbnail_image = thumnail_cover_image_resize(cover_file_obj)
        try:
            author = AuthorModel.objects.filter(author=user).get()
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

            try:
                PreAuthorPost.objects.filter(author=user).get()
                return Response(
                    {
                        "code": 415,
                        "message": kr_error_code(415)
                    }
                    , status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

            except ObjectDoesNotExist:

                created = PreAuthorPost.objects.create(
                    author=user,
                    title=temp.title,
                    main_content=temp.main_content,
                    price=data['price'],
                    preview=data['preview'],
                    cover_image=resizing_image,
                    thumbnail=thumbnail_image,
                )

                if created:
                    serializer = PostSerializer(created)

                    # 태그 추가 에외처리
                    if not self.search_tag(created, data['tag']):
                        return Response(
                            {
                                "code": 413,
                                "message": kr_error_code(413)
                            }
                            , status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

                    if data['recommend'] != '':
                        if not self.recommend_text(created, data['recommend']):
                            return Response(
                                {
                                    "code": 413,
                                    "message": kr_error_code(413)
                                }
                                , status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

                    # 템프파일 삭제 예외처리
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
                                "code": 409,
                                "message": kr_error_code(409)
                            }
                            , status=status.HTTP_409_CONFLICT)
                else:
                    return Response(
                        {
                            "code": 415,
                            "message": kr_error_code(415)
                        }
                        , status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        except ObjectDoesNotExist:
            result = AuthorModel.objects.get_or_create(author=user, intro=data['intro'], blog=data['blog'])
            if result:
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

                try:
                    PreAuthorPost.objects.filter(author=user).get()
                    return Response(
                        {
                            "code": 415,
                            "message": kr_error_code(415)
                        }
                        , status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

                except ObjectDoesNotExist:

                    created = PreAuthorPost.objects.create(
                        author=user, title=temp.title,
                        main_content=temp.main_content,
                        price=data['price'],
                        preview=data['preview'],
                        cover_image=resizing_image,
                        thumbnail=thumbnail_image,
                    )

                    if created:
                        serializer = PostSerializer(created)

                        # 태그 추가 에외처리

                        if data['tag'] != '':
                            if not self.search_tag(created, data['tag']):
                                return Response(
                                    {
                                        "code": 413,
                                        "message": kr_error_code(413)
                                    }
                                    , status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

                        if data['recommend'] != '':
                            if not self.recommend_text(created, data['recommend']):
                                return Response(
                                    {
                                        "code": 413,
                                        "message": kr_error_code(413)
                                    }
                                    , status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

                        # 템프파일 삭제 예외처리
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
                                    "code": 409,
                                    "message": kr_error_code(409)
                                }
                                , status=status.HTTP_409_CONFLICT)
                    else:
                        return Response(
                            {
                                "code": 415,
                                "message": kr_error_code(415)
                            }
                            , status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

            return Response(
                {
                    "code": 500,
                    "message": kr_error_code(500)
                }
                , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

