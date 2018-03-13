from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins, generics, status, exceptions
from rest_framework.parsers import  MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Temp, TempFile
from column.serializers.post import TempSerializer, TempFileSerializer

from member.models import Author as AuthorModel, User

__all__ = (
    'TempCreateView',
    'TempListView',
    'TempFileUpload',
    'TempView'
)


class TempView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        param = self.kwargs.get('pk')
        user =self.request.user
        if param:
            try:
                temp = Temp.objects.filter(user=user, pk=param).get()
                serializer = TempSerializer(temp)
                if serializer:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                raise exceptions.ValidationError({"detail":"Abnormal connnectd"})
            except ObjectDoesNotExist:
                raise exceptions.ValidationError({"detail":"Do not have temp"})
        else:
            try:
                Temp.objects.filter(user=user).order_by('-modified_date')
                return Response(True, 200)
            except ObjectDoesNotExist:
                return Response(False, 200)


class TempCreateView(generics.GenericAPIView,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Temp.objects.all()
    serializer_class = TempSerializer
    permission_classes = (IsAuthenticated,)

    def is_author(self):
        try:
            author = AuthorModel.objects.all().get(author_id=self.request.user.id)
            return author
        except ObjectDoesNotExist:
            author = None
            return author

    def temp_result(self, user):
        try:
            result = Temp.objects.all().get(author=user)
            return result
        except ObjectDoesNotExist:
            result = None
            return result

    def check_post_count(self, user):
        temp = Temp.objects.filter(author=user).count()
        if temp < 10:
            return True
            # return temp

    def post(self, request):
        user = self.request.user
        data = self.request.data

        # 1. 작가가 신청되어있는지 확인
        # 2. 작가 활성이 되어있는지를 확인
        # author = self.is_author()
        # if author is not None:
        #     if not author.is_active:
        #         raise exceptions.NotAcceptable({"detail": "This Account is Deactive"}, 401)
        # else:
        #     raise exceptions.NotAcceptable({"detail": "This Account is not Author"}, 401)

        # 1. 작성중인 포스트 검색
        # 2. 있다면 업데이트 없다면 생성

        # if data['id'] is None:
        #     return Response({"detail": "Abnormal Connect"}, status=status.HTTP_400_BAD_REQUEST)

        key = list(self.request.data.keys())

        if len(key) is not 3:
            raise exceptions.ValidationError({"detail": "Abnormal Connected"}, 406)

        if data['temp_id'] is not '':
            Temp.objects.filter(author=self.request.user, id=data['temp_id']).update(
                title=data['title'],
                main_content=data['main_content'])

            return Response({"temp": {
                "temp_id": data['temp_id']
            }}, status=status.HTTP_200_OK)

        else:
            # 임시 저장 할 수있는 게시물 제한
            checkcount = self.check_post_count(user)
            if not checkcount:
                raise exceptions.ValidationError({"detail": "This account exceeded the number of articles you could write"},
                                400)

            serializer = self.get_serializer(self.queryset.create(author=user, title=data['title'],
                                                                  main_content=data['main_content']))
            return Response({"temp": {
                "temp_id": serializer.data['id'],
            }}, status=status.HTTP_201_CREATED)

    # 임시저장 삭제
    def delete(self, request):
        user = self.request.user
        data = self.request.data

        key = list(self.request.data.keys())

        if len(key) is not 3:
            return Response({"detail": "Abnormal Connected"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        if data['temp_id'] is '':
            return Response({"detail": "Temp does not exist."}, status=status.HTTP_200_OK)
        return self.queryset.filter(author=user).delete(id=data['id'])


class TempFileUpload(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    serializer_class = TempFileSerializer

    def is_author(self):
        try:
            author = AuthorModel.objects.all().get(author_id=self.request.user.id)
            return author
        except ObjectDoesNotExist:
            author = None
            return author

    # 파일 업로드
    def post(self, request, *args, **kwargs):
        file_obj = self.request.FILES['files[]']

        # author = self.is_author()
        #
        # if author is not None:
        #     if not author.is_active:
        #         raise exceptions.NotAcceptable({"detail": "This Account is Deactive"}, 401)
        # else:
        #     raise exceptions.NotAcceptable({"detail": "This Account is not Author"}, 401)
        user = User.objects.filter(pk=self.request.user.id).get()

        serializer = TempFileSerializer(TempFile.objects.create(author=user, file=file_obj))
        if serializer:
            return Response({"files[0]":
                {
                    "id": serializer.data['id'],
                    "file": {
                        "url": serializer.data['file']
                    }
                }
            }, status=status.HTTP_201_CREATED)
        raise exceptions.APIException({"detail": "Upload Failed"}, 400)


class TempListView(generics.ListCreateAPIView):
    queryset = Temp.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TempSerializer

    # 임시저장된 문서를 보여주는 리스트 뷰
    def get(self, request, *args, **kwargs):
        author = self.request.user
        if not self.request.user.is_authenticated():
            raise exceptions.NotAuthenticated()

        result = Temp.objects.filter(author=author)
        serializer = self.get_serializer(result, many=True)

        if result is None:
            return Response({"detail": ""}, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)