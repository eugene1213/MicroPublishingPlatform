import base64

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, exceptions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from column.models import Temp, PreAuthorPost, Post, SearchTag, PreSearchTag

from column.serializers import PostSerializer, PreAuthorPostSerializer
from member.models import Author as AuthorModel, User, PointHistory
from member.serializers import AuthorSerializer
from octo.models import UsePoint
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
        raise exceptions.ValidationError({'detail': 'eEmpty image'}, status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED)

    def first_point(self):
        return UsePoint.objects.filter(type='first_user').get().point

    # 검색 태그 추가
    def search_tag(self, post, tag):
        search_tag = tag.split(',')
        if len(search_tag) > 5:
            raise exceptions.ValidationError({'detail': 'You can`t add up to 5'}, status.HTTP_406_NOT_ACCEPTABLE)

        for i in search_tag:
            PreSearchTag.objects.select_related('post').create(post=post, tag=i)

        return True

    # 작가 신청메서드
    def post(self, request):
        user = self.request.user
        data = self.request.data

        try:
            self.request.data['cover']
        except ObjectDoesNotExist:
            raise exceptions.NotAcceptable({'detail': 'Abnormal connected'})

        cover_file_obj = self.base64_content(self.request.data['cover'])
        resizing_image = image_quality_down(cover_file_obj)
        thumbnail_image = thumnail_cover_image_resize(cover_file_obj)
        try:
            author = AuthorModel.objects.filter(author=user).get()
            # 임시저장 파일이 없을 경우
            if data['temp_id'] == '':
                raise exceptions.NotAcceptable({'detail': 'Abnormal connected'})

            try:
                temp = Temp.objects.filter(id=data['temp_id']).get()

            except ObjectDoesNotExist:
                raise exceptions.PermissionDenied({'detail': 'Already Posted or temp not exist'})

            try:
                PreAuthorPost.objects.filter(author=user).get()
                print(2)
                raise exceptions.NotAcceptable({'detail': 'Already processing author is_active'})

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
                    if not self.search_tag(post=created, tag=self.request.data['tag']):
                        raise exceptions.PermissionDenied({'detail': 'Upload tag Failed'})

                    # 템프파일 삭제 예외처리
                    try:
                        Temp.objects.filter(id=data['temp_id']).delete()

                    except ObjectDoesNotExist:
                        raise exceptions.PermissionDenied({'detail': 'Already Posted or temp not exist'})

                # 태그를 추가하고 태그 추가 실패

                    if serializer:
                        return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)
                    else:
                        raise exceptions.ParseError({'detail': 'Already added'})
                else:
                    print(3)
                    raise exceptions.NotAcceptable({'detail': 'Already processing author is_active'})

        except ObjectDoesNotExist:
            result = AuthorModel.objects.get_or_create(author=user, intro=data['intro'], blog=data['blog'])
            if result:
                if data['temp_id'] == '':
                    raise exceptions.PermissionDenied({'detail': 'Abnormal connected'})
                try:
                    temp = Temp.objects.filter(id=data['temp_id']).get()

                except ObjectDoesNotExist:
                    raise exceptions.PermissionDenied({'detail': 'Already Posted or temp not exist'})

                try:
                    PreAuthorPost.objects.filter(author=user).get()
                    print(6)
                    raise exceptions.NotAcceptable({'detail': 'Already processing author is_active'})

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
                        if not self.search_tag(post=created, tag=self.request.data['tag']):
                            raise exceptions.NotAcceptable({'detail': 'Upload tag Failed'})

                        # 템프파일 삭제 예외처리
                        try:
                            Temp.objects.filter(id=data['temp_id']).delete()

                        except ObjectDoesNotExist:
                            raise exceptions.NotAcceptable({'detail': 'Already Posted or temp not exist'})

                        # 태그를 추가하고 태그 추가 실패

                        if serializer:
                            return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)
                        else:
                            raise exceptions.NotAcceptable({'detail': 'Already added'})
                    else:
                        print(2)
                        raise exceptions.NotAcceptable({'detail': 'Already processing author is_active'})

            raise exceptions.ValidationError({'detail': 'Abnormal connected'})

