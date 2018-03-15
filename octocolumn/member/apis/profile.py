import base64

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from rest_framework import generics, status, exceptions
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Post, Temp
from column.serializers import PostSerializer, TempSerializer
from member.models import ProfileImage, Profile
from member.serializers import ProfileImageSerializer, ProfileSerializer

__all__ = (
    'ProfileImageUpload',
    'UserCoverImageUpload',
    'ProfileInfo',
    'ProfileIntroUpdate',
    'PublishPost',
    'MyTemp'
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
            raise exceptions.ValidationError({"detail": "Abnormal connected"})
        except ObjectDoesNotExist:

            return Response({"nickname": user.nickname,
                             "waiting": user.waiting_count,
                             "post_count": Post.objects.filter(author=user).count(),
                             "intro": "-",
                             "following": user.following_users_count,
                             "follower": user.follower_users_count,
                             "image": {
                                 "profile_image": "/static/images/example/1.jpeg",
                                "cover_image": "/static/images/example/2/jpeg"
                             }
                             }, status=status.HTTP_200_OK)


class ProfileIntroUpdate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = self.request.user
        data = self.request.data

        try:
            profile = Profile.objects.filter(user=user).get()

            profile.intro = data['userIntro']
            profile.save()
            serializer = ProfileSerializer(profile)

            if serializer:
                return Response('', status=status.HTTP_200_OK)
            raise exceptions.ValidationError({"detail": "Abnormal connected"})

        except ObjectDoesNotExist:
            update = Profile.objects.create(user=user, intro=data['userIntro'])
            serializer = ProfileSerializer(update)

            if serializer:
                return Response('', status=status.HTTP_200_OK)
            raise exceptions.ValidationError({"detail": "Abnormal connected"})


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
        user = self.request.user
        profile_file_obj = self.base64_content(self.request.data)

        try:
            profile_image = ProfileImage.objects.filter(user=user).get()
            profile_image.profile_image = profile_file_obj
            profile_image.save()

            serializer = ProfileImageSerializer(profile_image)
            if serializer:
                return Response({"fileUpload": serializer.data}, status=status.HTTP_201_CREATED)
            raise exceptions.APIException({"detail": "Upload Failed"}, 400)

        except ObjectDoesNotExist:
            serializer = ProfileImageSerializer(ProfileImage.objects.create(user=user,
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
        user = self.request.user
        cover_file_obj = self.base64_content(self.request.data)
        try:
            profile_image = ProfileImage.objects.filter(user=user).get()
            profile_image.cover_image = cover_file_obj
            profile_image.save()
            serializer = ProfileImageSerializer(profile_image)
            if serializer:
                return Response({"fileUpload": serializer.data}, status=status.HTTP_201_CREATED)
            raise exceptions.APIException({"detail": "Upload Failed"}, 400)

        except ObjectDoesNotExist:
            serializer = ProfileImageSerializer(ProfileImage.objects.create(user=user,
                                                                            cover_image=cover_file_obj))
            if serializer:
                return Response({"fileUpload": serializer.data}, status=status.HTTP_201_CREATED)
            raise exceptions.APIException({"detail": "Upload Failed"}, 400)


class PublishPost(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = self.request.user

        try:
            post = Post.objects.filter(author=user).order_by('created_date').all()
            serializer = PostSerializer(post, many=True)
            if serializer:
                return Response({"join_date": user.created_at, "post": serializer.data}, status=status.HTTP_200_OK)
            raise exceptions.APIException({"detail": "Abnormal connected"}, 400)

        except ObjectDoesNotExist:
            return None


class MyTemp(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = self.request.user

        try:
            temp = Temp.objects.filter(author=user).order_by('-created_date').all()
            serializer = TempSerializer(temp, many=True)
            if serializer:
                return Response({"post": serializer.data}, status=status.HTTP_200_OK)
            raise exceptions.APIException({"detail": "Abnormal connected"}, 400)

        except ObjectDoesNotExist:
            return None


