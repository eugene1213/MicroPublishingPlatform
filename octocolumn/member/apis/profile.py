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
        profile_file_obj = self.base64_content(self.request.data['profile'])
        cover_file_obj = self.base64_content(self.request.data['profile_cover'])

        serializer = ProfileImageSerializer(ProfileImage.objects.create(user=self.request.user,
                                                                        profile_image=profile_file_obj,
                                                                        cover_image=cover_file_obj))
        if serializer:
            return Response({"fileUpload": serializer.data}, status=status.HTTP_201_CREATED)
        raise exceptions.APIException({"detail": "Upload Failed"}, 400)
