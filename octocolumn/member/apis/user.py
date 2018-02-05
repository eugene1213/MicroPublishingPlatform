from http import cookies
from pprint import pprint
from typing import NamedTuple

import requests
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from member.backends import FacebookBackend
from member.models import User
from member.serializers import UserSerializer, SignUpSerializer


__all__ = (
    'Login',
    'SignUpAPIView',
    'SignUp',
    'FacebookLogin'
)


class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(
            username=username,
            password=password,
        )
        if user:
            # 'user'키에 다른 dict로 유저에 대한 모든 정보를 보내줌
            token, token_created = Token.objects.get_or_create(user=user)
            C = cookies.BaseCookie()

            C["token"] = token.key
            C["token"].httpOnly = None
            data = {
                'token': token.key,
                'user': UserSerializer(user).data,
                'cookie': print(C),
                'cookie_detail': C
            }

            return Response(data, status=status.HTTP_200_OK)

        data = {
            'message': 'Invalid credentials'
        }

        return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class SignUp(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class SignUpAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FacebookLogin(APIView):
    # /api/member/facebook-login/
    def post(self, request):
        # request.data에
        #   access_token
        #   facebook_user_id
        #       데이터가 전달됨

        # Debug결과의 NamedTuple
        class DebugTokenInfo(NamedTuple):
            app_id: str
            application: str
            expires_at: int
            is_valid: bool
            scopes: list
            type: str
            user_id: str

        # token(access_token)을 받아 해당 토큰을 Debug
        def get_debug_token_info(token):
            app_id = settings.FACEBOOK_APP_ID
            app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
            app_access_token = f'{app_id}|{app_secret_code}'

            url_debug_token = 'https://graph.facebook.com/debug_token'
            params_debug_token = {
                'input_token': token,
                'access_token': app_access_token,
            }
            response = requests.get(url_debug_token, params_debug_token)
            pprint(response.json())
            return DebugTokenInfo(**response.json()['data'])

        # request.data로 전달된 access_token값을 페이스북API쪽에 debug요청, 결과를 받아옴
        debug_token_info = get_debug_token_info(request.data['access_token'])

        if debug_token_info.user_id != request.data['facebook_user_id']:
            raise APIException('페이스북 토큰의 사용자와 전달받은 facebook_user_id가 일치하지 않음')

        if not debug_token_info.is_valid:
            raise APIException('페이스북 토큰이 유효하지 않음')

        # FacebookBackend를 사용해서 유저 인증
        user = FacebookBackend.authenticate(facebook_user_id=request.data['facebook_user_id'])
        # 인증에 실패한 경우 페이스북유저 타입으로 유저를 만들어줌
        if not user:
            user = User.objects.create_user(
                username=f'fb_{request.data["facebook_user_id"]}',
                user_type=User.USER_TYPE_FACEBOOK,
                age=0,
            )
        # 유저 시리얼라이즈 결과를 Response
        # token도 추가
        data = {
            'user': UserSerializer(user).data,
            'token': user.token,
        }
        return Response(data)
#
#
# class GoogleLogin(APIView):
#     def post(self, request):
#         # request.data에
#         #   access_token
#         #   facebook_user_id
#         #       데이터가 전달됨
#         class DebugTokenInfo(NamedTuple):
#             client_id: str
#             redirect_uri: str
#             response_type: int
#             is_valid: bool
#             scopes: list
#             type: str
#             user_id: str
#
#         # token(access_token)을 받아 해당 토큰을 Debug
#         def get_debug_token_info(token):
#             app_id = settings.FACEBOOK_APP_ID
#             app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
#             app_access_token = f'{app_id}|{app_secret_code}'
#
#             url_debug_token = 'https://graph.facebook.com/debug_token'
#             params_debug_token = {
#                 'input_token': token,
#                 'access_token': app_access_token,
#             }
#             response = requests.get(url_debug_token, params_debug_token)
#             pprint(response.json())
#             return DebugTokenInfo(**response.json()['data'])
#
#         # request.data로 전달된 access_token값을 페이스북API쪽에 debug요청, 결과를 받아옴
#         debug_token_info = get_debug_token_info(request.data['access_token'])
#
#         if debug_token_info.user_id != request.data['facebook_user_id']:
#             raise APIException('페이스북 토큰의 사용자와 전달받은 facebook_user_id가 일치하지 않음')
#
#         if not debug_token_info.is_valid:
#             raise APIException('페이스북 토큰이 유효하지 않음')
#
#         # FacebookBackend를 사용해서 유저 인증
#         user = FacebookBackend.authenticate(facebook_user_id=request.data['facebook_user_id'])
#         # 인증에 실패한 경우 페이스북유저 타입으로 유저를 만들어줌
#         if not user:
#             user = User.objects.create_user(
#                 username=f'fb_{request.data["facebook_user_id"]}',
#                 user_type=User.USER_TYPE_FACEBOOK,
#                 age=0,
#             )
#         # 유저 시리얼라이즈 결과를 Response
#         # token도 추가
#         data = {
#             'user': UserSerializer(user).data,
#             'token': user.token,
#         }
#         return Response(data)
#
#     pass
#
#
# class TwitterLogin(APIView):
#     def post(self, request):
#         pass
#
#     pass


class TokenUserInfoAPIView(APIView):
    def post(self, request):
        token_string = request.data.get('token')
        try:
            token = Token.objects.get(key=token_string)
        except Token.DoesNotExist:
            raise APIException('token invalid')
        user = token.user
        return Response(UserSerializer(user).data)


class UserDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk=None):
        return Response(UserSerializer(request.user).data)


class FileUploadView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.FILES['file']
        User.objects.filter(user=self.request.user).create(file=file_obj)
        # do some stuff with uploaded file
        return Response({"detail":"Upload Success"},status=204)
