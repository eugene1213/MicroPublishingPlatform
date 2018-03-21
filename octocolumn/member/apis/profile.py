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
from member.models.user import WaitingRelation, Relation
from member.serializers import ProfileImageSerializer, ProfileSerializer

__all__ = (
    'ProfileImageUpload',
    'UserCoverImageUpload',
    'ProfileInfo',
    'ProfileIntroUpdate',
    'PublishPost',
    'MyTemp',
    'ProfileUpdate'
)


# 1
# 유저의 프로필을 가져오는 API
# URL /api/member/getProfileInfo/
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
            try:
                profile_image = ProfileImage.objects.filter(user=user).get()

                serializer = ProfileImageSerializer(profile_image)
                return Response({"nickname": user.nickname,
                                 "waiting": WaitingRelation.objects.filter(receive_user=user).count(),
                                 "post_count": Post.objects.filter(author=user).count(),
                                 "point": user.point,
                                 "intro": "-",
                                 "following": Relation.objects.filter(from_user=user).count(),
                                 "follower": Relation.objects.filter(to_user=user).count(),
                                 "image": serializer.data

                                 }, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({"nickname": user.nickname,
                             "waiting": WaitingRelation.objects.filter(receive_user=user).count(),
                             "post_count": Post.objects.filter(author=user).count(),
                             "point": user.point,
                             "intro": "-",
                             "following": Relation.objects.filter(from_user=user).count(),
                             "follower": Relation.objects.filter(to_user=user).count(),
                             "image": {
                                 "profile_image": "/static/images/example/2_x20_.jpeg",
                                "cover_image": "/static/images/example/1.jpeg"
                             }
                             }, status=status.HTTP_200_OK)


# 1
# 유저의 프로필중 자기소개를 업데이트 하는 API
# URL /api/member/updateProfileIntro/
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

            # 데이터를 직렬화 시켜 프린트
            if serializer:
                return Response('', status=status.HTTP_200_OK)
            raise exceptions.ValidationError({"detail": "Abnormal connected"})

        except ObjectDoesNotExist:
            update = Profile.objects.create(user=user, intro=data['userIntro'])
            serializer = ProfileSerializer(update)

            if serializer:
                return Response('', status=status.HTTP_200_OK)
            raise exceptions.ValidationError({"detail": "Abnormal connected"})


# 1
# 유저의 프로필중 자기소개를 업데이트 하는 API
# URL /api/member/updateProfile/
class ProfileUpdate(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = self.request.user
        data = self.request.data

        try:
            profile = Profile.objects.filter(user=user).get()

            profile.year = data['birthYear']
            profile.month = data['birthMonth']
            profile.day = data['birthDay']
            profile.sex = data['sex']
            profile.phone = data['hpNumber']
            profile.age = data['age']
            profile.web = data['web']
            profile.jobs = data['job']
            profile.region =data['region']
            profile.facebook = data['fb']
            profile.instagram = data['ins']
            profile.twitter = data['tw']
            profile.subjects = data['subject']
            profile.save()
            return Response('', status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            if Profile.objects.create(
                    user=user, year=data['bithYear'], month=data['bithMonth'], day=data['bithDay'], sex=data['sex'],
                    phone=data['hpNumber'], age=data['age'],job=data['job'], facebook=data['fb'], instagram=data['ins'],
                    twitter=data['tw'], subjects=data['subject']):
                return Response(status=status.HTTP_200_OK)
            raise exceptions.ValidationError('Abnormal connectd')


# 1
# 유저의 프로필중 프로필이미지를를 업데이트 하는 API
# URL /api/member/profile-image/
class ProfileImageUpload(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)
    serializer_class = ProfileImageSerializer

    # base64 파일 파일 형태로
    def base64_content(self, image, size):
        if image is not '':
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=size+'.'+ext)
            return data
        raise exceptions.ValidationError({'detail': 'eEmpty image'}, 400)

    #파일 업로드
    def post(self, request,*args,**kwargs):
        user = self.request.user
        size = self.request.data['margin']
        profile_file_obj = self.base64_content(self.request.data['img'], size)

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


# 1
# 유저의 프로필중 커버이미지를 업데이트 하는 API
# URL /api/member/usercover-image/
class UserCoverImageUpload(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)
    serializer_class = ProfileImageSerializer

    # base64 파일 파일 형태로
    def base64_content(self, image, size):
        if image is not '':
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=size+'.'+ext)
            return data
        raise exceptions.ValidationError({'detail': 'eEmpty image'}, 400)

    def post(self, request,*args,**kwargs):
        user = self.request.user
        size = self.request.data['margin']
        cover_file_obj = self.base64_content(self.request.data['img'], size)

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
                                                                            cover_image=cover_file_obj + size))
            if serializer:
                return Response({"fileUpload": serializer.data}, status=status.HTTP_201_CREATED)
            raise exceptions.APIException({"detail": "Upload Failed"}, 400)


# 1
# 유저의 프로필중 자기가 발행한 컬럼들을 리스팅 하는 API
# URL /api/member/getMyPost/
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


# 1
# 유저의 프로필중 자기가 임시저장된 컬럼들을 리스팅 하는 API
# URL /api/member/getMyTemp/
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


class InviteUser(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self):
        user = self.request.user