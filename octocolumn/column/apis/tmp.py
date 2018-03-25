from datetime import datetime
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


# 1
class TempView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        param = self.kwargs.get('pk')
        user = self.request.user

        if param:
            try:
                temp = Temp.objects.filter(author=user, pk=param).get()
                serializer = TempSerializer(temp)
                if serializer:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                raise exceptions.ValidationError({"detail":"Abnormal connnectd"})
            except ObjectDoesNotExist:
                raise exceptions.ValidationError({"detail": "Do not have temp"})
        else:
            try:
                temp = Temp.objects.filter(author=user).order_by('-created_date')[:1].get()
                serializer = TempSerializer(temp)
                if serializer:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                raise exceptions.ValidationError({"detail": "Abnormal connnectd"})
            except ObjectDoesNotExist:
                return Response('', 200)


# 1
class TempCreateView(generics.GenericAPIView,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Temp.objects.all()
    serializer_class = TempSerializer
    permission_classes = (IsAuthenticated,)

    def is_author(self):
        try:
            author = AuthorModel.objects.filter(author=self.request.user).get()
            return author
        except ObjectDoesNotExist:
            author = None
            return author

    # 임시저장 카운트 갯수
    def check_post_count(self, user):
        temp = Temp.objects.filter(author=user).count()
        if temp < 10:
            return True
        return False

    def post(self, request):
        user = self.request.user
        data = self.request.data

        if self.request.data.get('temp_id') is None:
            raise exceptions.ValidationError({"detail": "Abnormal Connected"}, 406)

        if data['temp_id'] is not '':
            Temp.objects.filter(author=self.request.user, id=data['temp_id']).update(title=data['title'],
                                                                                     main_content=data['main_content'],
                                                                                     created_date=datetime.now()
                                                                                     )

            return Response({"temp": {
                "temp_id": data['temp_id']
            }}, status=status.HTTP_200_OK)

        else:
            # 임시 저장 할 수있는 게시물 제한
            if not self.check_post_count(user):
                raise exceptions.ValidationError({"detail": "This account exceeded the number of articles you could write"},
                                                 400)
            temp = self.queryset.create(author=user, title=data['title'], main_content=data['main_content'])

            # 예외처리
            if not temp:
                raise exceptions.ValidationError({"detail": "Critical Error"}, 406)

            serializer = self.get_serializer(temp)
            if serializer:
                return Response({"temp": {
                    "temp_id": serializer.data['id'],
                }}, status=status.HTTP_201_CREATED)
            raise exceptions.ValidationError({"detail": "Abnormal Connected"}, 406)

    # 임시저장 삭제
    def delete(self, request):
        user = self.request.user
        data = self.request.data
        # request.data 에 temp_id 없을시 에러 발생
        if self.request.data.get('temp_id') is None:
            raise exceptions.ValidationError({"detail": "Abnormal Connected"}, 406)

        if data['temp_id'] is '':
            raise exceptions.ValidationError({"detail": "Temp does not exist."})
        return self.queryset.filter(author=user).delete(id=data['temp_id'])


# 1
class TempFileUpload(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    serializer_class = TempFileSerializer

    # 파일 업로드
    def post(self, request, *args, **kwargs):
        user = self.request.user
        file_obj = self.request.FILES['files[]']

        temp_file = TempFile.objects.create(author=user, file=file_obj)
        # 예외처리
        if not temp_file:
            raise exceptions.ValidationError({"detail": "Upload Failed"})

        serializer = TempFileSerializer(temp_file)
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


# 1
class TempListView(generics.ListCreateAPIView):
    queryset = Temp.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TempSerializer

    # 임시저장된 문서를 보여주는 리스트 뷰
    def get(self, request, *args, **kwargs):
        user = self.request.user

        result = Temp.objects.filter(author=user).all()
        serializer = self.get_serializer(result, many=True)

        if result is None:
            return Response({"detail": ""}, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)