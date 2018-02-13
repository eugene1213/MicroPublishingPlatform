from rest_framework import generics, status, exceptions
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from member.models import ProfileImage
from member.serializers import ProfileImageSerializer


class ProfileImageUpload(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser,)
    serializer_class = ProfileImageSerializer

    #파일 업로드
    def post(self, request,*args,**kwargs):
        file_obj = self.request.FILES['files[]']

        serializer = ProfileImageSerializer(ProfileImage.objects.create(author=self.request.user ,file=file_obj))
        if serializer:
            return Response({"fileUpload": serializer.data}, status=status.HTTP_201_CREATED)
        raise exceptions.APIException({"detail": "Upload Failed"}, 400)
