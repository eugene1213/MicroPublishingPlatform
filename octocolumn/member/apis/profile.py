import base64

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from rest_framework import generics, status, exceptions
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import ProfileImage, Profile
from member.serializers import ProfileImageSerializer, ProfileSerializer

__all__ = (
    'ProfileImageUpload',
    'UserCoverImageUpload',
    'ProfileInfo'
)


class ProfileInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = self.request.user
        try:
            profile = Profile.objects.filter(user=user).get()
            serializer = ProfileSerializer(profile)

            if serializer:
                return Response(serializer.data, status=status.HTTP_200_OK)
            raise exceptions.ValidationError({"detail":"Abnormal connected"})
        except ObjectDoesNotExist:
            raise exceptions.ValidationError({"detail": "You have not entered yet."})


class ProfileImageUpload(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)
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
        profile_file_obj = self.base64_content(self.request.data)

        serializer = ProfileImageSerializer(ProfileImage.objects.update_or_create(user=self.request.user,
                                                                        profile_image=profile_file_obj))

        if serializer:
            return Response({"fileUpload": serializer.data}, status=status.HTTP_201_CREATED)
        raise exceptions.APIException({"detail": "Upload Failed"}, 400)


class UserCoverImageUpload(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)
    serializer_class = ProfileImageSerializer

    # base64 파일 파일 형태로
    def base64_content(self, image):
        if image is not '':
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            return data
        raise exceptions.ValidationError({'detail': 'eEmpty image'}, 400)

    def post(self, request,*args,**kwargs):
        print(request.data)
        cover_file_obj = self.base64_content(self.request.data)

        serializer = ProfileImageSerializer(ProfileImage.objects.update_or_create(user=self.request.user,
                                                                                  cover_image=cover_file_obj))
        if serializer:
            return Response({"fileUpload": serializer.data}, status=status.HTTP_201_CREATED)
        raise exceptions.APIException({"detail": "Upload Failed"}, 400)

