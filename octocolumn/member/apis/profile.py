import base64

from django.core.files.base import ContentFile
from rest_framework import generics, status, exceptions
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from member.models import ProfileImage
from member.serializers import ProfileImageSerializer, CoverImageSerializer

__all__ = (
    'ProfileImageUpload',
    'UserCoverImageUpload'
)


class ProfileImageUpload(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    serializer_class = ProfileImageSerializer

    # base64 파일 파일 형태로
    def base64_content(self, image):
        if image is not '':
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            return data
        raise exceptions.ValidationError({'detail': 'eEmpty image'}, 400)

    #파일 업로드
    def post(self, request,*args,**kwargs):
        profile_file_obj = self.base64_content(self.request.data['img'])

        serializer = ProfileImageSerializer(ProfileImage.objects.update_or_create(user=self.request.user,
                                                                        profile_image=profile_file_obj))

        if serializer:
            return Response({"fileUpload": serializer.data}, status=status.HTTP_201_CREATED)
        raise exceptions.APIException({"detail": "Upload Failed"}, 400)


class UserCoverImageUpload(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    serializer_class = CoverImageSerializer

    # base64 파일 파일 형태로
    def base64_content(self, image):
        if image is not '':
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            return data
        raise exceptions.ValidationError({'detail': 'eEmpty image'}, 400)

    def post(self, request,*args,**kwargs):
        cover_file_obj = self.base64_content(self.request.data['img'])

        serializer = ProfileImageSerializer(ProfileImage.objects.update_or_create(user=self.request.user,
                                                                                  cover_file_obj=cover_file_obj))
        if serializer:
            return Response({"fileUpload": serializer.data}, status=status.HTTP_201_CREATED)
        raise exceptions.APIException({"detail": "Upload Failed"}, 400)

