import base64

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from rest_framework import generics, mixins, exceptions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from column.models import Temp, PreAuthorPost, Post, SearchTag
from column.serializers import PostSerializer, PreAuthorPostSerializer
from member.models import Author as AuthorModel, User, PointHistory
from member.serializers import AuthorSerializer
from octo.models import UsePoint

__all__ = (
    'AuthorApply',
)


# 1
class AuthorApply(generics.GenericAPIView,
             mixins.ListModelMixin,
             mixins.CreateModelMixin,
             mixins.DestroyModelMixin):
    permission_classes = (IsAuthenticated, )
    queryset = AuthorModel.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return User.objects.filter(username=self.request.user)
        else:
            raise exceptions.NotAuthenticated()

    # base64 파일 파일 형태로
    def base64_content(self, image):
        if image is not '':
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            return data
        raise exceptions.ValidationError({'detail': 'eEmpty image'}, 400)

    def search_tag(self, post, tag):
        search_tag = tag.split(',')
        if len(search_tag) > 5:
            raise exceptions.ValidationError({'detail': 'You can`t add up to 5'}, 200)

        for i in search_tag:
            SearchTag.objects.create(post=post, tag=i)

        return True

    def first_point(self):
        return UsePoint.objects.filter(type='first_user').get().point

    #작가 신청메서드
    def post(self, request):
        user = self.request.user
        data = self.request.data

        if AuthorModel.objects.filter(author=user).get() is not None:
            raise exceptions.ValidationError({"datail":"Already Apply"})

        author, result = AuthorModel.objects.get_or_create(author=user, intro=data['intro'], blog=data['blog'])

        if result:

            preview_file_obj = self.base64_content(self.request.data['preview'])
            cover_file_obj = self.base64_content(self.request.data['cover'])

            # 임시저장 파일이 없을 경우
            if data['temp_id'] == '':
                raise exceptions.NotAcceptable({'detail': 'Abnormal connected'}, 400)
            try:
                temp = Temp.objects.filter(id=data['temp_id']).get()
            except ObjectDoesNotExist:
                raise exceptions.NotAcceptable({'detail': 'Already Posted or temp not exist'}, 400)
            # 포인트가 모자르다면 에러발생
            if 300 > user.point:
                raise exceptions.NotAcceptable({"detail": "There is not enough points."}, 400)

            # 클로즈 베타 끝나고 -> PreAuthorpost 변경
            post = Post.objects.create(author=user, title=temp.title,
                                       main_content=temp.main_content,
                                       price=data['price'],
                                       preview_image=preview_file_obj,
                                       cover_image=cover_file_obj,

                                       )
            # 클로즈 베타 끝나고 -> PreAuthorpost 변경
            serializer = PostSerializer(post)

            # 태그 추가 에외처리
            if not self.search_tag(post=post, tag=self.request.data['tag']):
                raise exceptions.ValidationError({'detail': 'Upload tag Failed'}, 400)

            # 템프파일 삭제 예외처리
            try:
                Temp.objects.filter(id=data['temp_id']).delete()
            except ObjectDoesNotExist:
                raise exceptions.ValidationError({'detail': 'Already Posted or temp not exist'}, 400)

            # 포인트 내역 추가 예외처리 완료
            point_history = PointHistory.objects.publish(user=self.request.user, point=self.first_point(), post=post,
                                                         history=temp.title)
            if not point_history:
                raise exceptions.ValidationError({'detail': 'Upload Failed'})

            user.point -= self.first_point()
            user.save()
            # 태그를 추가하고 태그 추가 실패

            if serializer:
                return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)
            else:
                raise exceptions.ValidationError({'detail': 'Already added'}, 400)

        else:
            raise exceptions.ValidationError({'detail': 'Already attempted author'}, 400)




