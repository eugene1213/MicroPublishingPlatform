import token
from pprint import pprint

import requests
from django.contrib.auth import authenticate, logout
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import NamedTuple

from config import settings
from member.backends import FacebookBackend
from member.models import User
from member.serializers import UserSerializer, SignUpSerializer
from member.serializers.user import ChangePasswordSerializer
from utils.jwt import jwt_token_generator

__all__ = (
    'Login',
    'SignUp',
    'Logout',
    'FacebookLogin',
    'UpdatePassword'
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

            data = {
                'token': jwt_token_generator(user),
                'user': UserSerializer(user).data,
            }

            return Response(data, status=status.HTTP_200_OK)

        data = {
            'message': 'Invalid credentials'
        }

        return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            request.auth.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        logout(request)
        return Response({"detail": "Successfully logged out."},
                        status=status.HTTP_200_OK)


class SignUp(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class FacebookLogin(APIView):
    permission_classes = (AllowAny,)
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

        userid = debug_token_info.user_id

        userinfo = User.objects.filter(username=request.data['email']).count()

        if not userinfo == 0:
            raise APIException('Already exists this email')

        # FacebookBackend를 사용해서 유저 인증
        user = FacebookBackend.authenticate(facebook_user_id=userid)
        # 인증에 실패한 경우 페이스북유저 타입으로 유저를 만들어줌
        if not user:
            user = User.objects.create_facebook_user(
                username=request.data['email'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                social_id=f'fb_{request.data["facebook_user_id"]}',
                )

        # 유저 시리얼라이즈 결과를 Response
        # token도 추가
        data = {
            'user': UserSerializer(user).data,
            'token': jwt_token_generator(user),
        }
        return Response(data)


class TokenUserInfoAPIView(APIView):
    def post(self, request):
        token_string = request.data.get('token')
        try:
            token = Token.objects.get(key=token_string)
        except Token.DoesNotExist:
            raise APIException('token invalid')
        user = token.user
        return Response(UserSerializer(user).data)


class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, queryset=None):
        if self.request.user.user_type is not 'd':
            raise APIException('소셜계정은 비밀번호를 변경할수 없습니다.')
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecoveryPassword(APIView):
    def post(self):
        pass


class VerifyToken(APIView):
    def get(self):
        pass