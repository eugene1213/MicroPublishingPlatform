from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework import mixins, generics, status, exceptions
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Temp, TempFile
from column.serializers.post import TempSerializer, TempFileSerializer

from member.models import Author as AuthorModel

__all__ = (
    'TempCreateView',
)


class TempCreateView(generics.GenericAPIView,
             mixins.ListModelMixin,
             mixins.CreateModelMixin,
             mixins.DestroyModelMixin):
    queryset = Temp.objects.all()
    serializer_class = TempSerializer
    permission_classes = (AllowAny,)

    def is_author(self):
        try:
            author = AuthorModel.objects.all().get(author_id=self.request.user.id)
            return author
        except ObjectDoesNotExist:
            author = None
            return author

    def temp_result(self,user):
        try:
            result = Temp.objects.all().get(author=user)
            return result
        except ObjectDoesNotExist:
            result = None
            return result

    def check_post_count(self,user):
        temp = Temp.objects.filter(author=user).count()
        if temp < 10:
            return True
        # return temp

    def post(self, request):
            user = self.request.user
            data = self.request.data

            # 임시 저장 할 수있는 게시물 제한
            checkcount = self.check_post_count(user)
            if not checkcount:
                return Response({"detail": "This account exceeded the number of articles you could write"},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            # 1. 작가가 신청되어있는지 확인
            # 2. 작가 활성이 되어있는지를 확인
            author = self.is_author()
            if author is not None:
                if not author.is_active:
                    return Response({"detail": "This Account is Deactive"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"detail": "This Account is not Author"}, status=status.HTTP_401_UNAUTHORIZED)

            # 1. 작성중인 포스트 검색
            # 2. 있다면 업데이트 없다면 생성

            if data['id'] is not '':
                if data['id'] is None:
                    serializer = self.get_serializer(self.queryset.create(author=user, title=data['title'],
                                                                          main_content=data['main_content']))
                    return Response({"temp": serializer.data}, status=status.HTTP_201_CREATED)
                else:

                    Temp.objects.filter(author=self.request.user, id=data['id']).update(
                        title=data['title'],
                        main_content=data['main_content'])

                    return Response({"temp":''}, status=status.HTTP_200_OK)
            else:
                serializer = self.get_serializer(self.queryset.create(author=user, title=data['title'],
                                                                      main_content=data['main_content']))
                return Response({"temp": serializer.data}, status=status.HTTP_201_CREATED)

    # 임시저장 삭제
    def delete(self, request):
        user = self.request.user
        data = self.request.data

        if data['id'] is None:
            return Response({"detail": "Post does not exist."}, status=status.HTTP_200_OK)
        return self.queryset.filter(author=user).delete(id=data['id'])


class TempFileUpload(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser,)
    serializer_class = TempFileSerializer

    def is_author(self):
        try:
            author = AuthorModel.objects.all().get(author_id=self.request.user.id)
            return author
        except ObjectDoesNotExist:
            author = None
            return author

    #파일 업로드
    def post(self, request,*args,**kwargs):
        file_obj = self.request.FILES['files[]']

        author = self.is_author()

        if author is not None:
            if not author.is_active:
                return Response({"detail": "This Account is Deactive"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "This Account is not Author"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = TempFileSerializer(TempFile.objects.create(author=self.request.user ,file=file_obj))
        if serializer:
            return Response({"fileUpload": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"fileUpload": "Upload Failed"},status=status.HTTP_400_BAD_REQUEST)


class TempListView(generics.ListCreateAPIView):
    queryset = Temp.objects.all()
    serializer_class = TempSerializer

    # 임시저장된 문서를 보여주는 리스트 뷰
    def get(self, request, *args, **kwargs):
        author = self.request.user
        if not self.request.user.is_authenticated():
            raise exceptions.NotAuthenticated()

        result = Temp.objects.filter(author=author)
        serializer = self.get_serializer(result,many=True)

        if result is None:
            return Response({"detail": ""}, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)
