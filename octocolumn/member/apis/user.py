from django.core.exceptions import ObjectDoesNotExist
import requests
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from ipware.ip import get_ip
from redis_cache import cache

from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import NamedTuple

from rest_framework_jwt.settings import api_settings

from config import settings
from member.backends import FacebookBackend
from member.models import User, ProfileImage, ConnectedLog, InviteUser
from member.models.invitations import InvitationUser
from member.serializers import UserSerializer, SignUpSerializer, ProfileImageSerializer
from member.serializers.user import ChangePasswordSerializer
from member.task import PasswordResetTask, InviteUserTask
from utils.customsendmail import invite_email_send, password_reset_email_send
from utils.error_code import kr_error_code
from utils.jwt import jwt_token_generator
from utils.tokengenerator import account_activation_token

__all__ = (
    'Login',
    'SignUp',
    'Logout',
    'FacebookLogin',
    'PasswordReset',
    'SendInviteEmail',
    'PasswordResetSendEmail',
    'UserInfo',
    'InvitationUserView'
)


# 1
# 로그인 API
# URL /api/member/login/
# 전달 키값 : username, password
class Login(APIView):
    permission_classes = (AllowAny,)

    def saved_login_log(self, user):
        log = ConnectedLog()
        log.user = user
        log.type = 'login'
        log.ip_address = get_ip(self.request)
        log.user_agent = self.request.META['HTTP_USER_AGENT']
        return log.save()

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

            if data['user']['is_active']:
                response = Response(data, status=status.HTTP_200_OK)
                # response = render_to_response("view/main.html", {"login": True})
                # response = HttpResponseRedirect(redirect_to='/')
                if api_settings.JWT_AUTH_COOKIE:
                    response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                        data['token'],
                                        max_age=21600,
                                        httponly=True)
                    self.saved_login_log(user)
                    return response
                # return response
                return response
            data = {
                "detail": "This Account is not Activate"
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            # return HttpResponseRedirect(redirect_to='/signin/')
        data = {
            'detail': 'Invalid credentials'
        }

        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        # return HttpResponseRedirect(redirect_to='/signin/')


# 1
# 로그아웃 API
# URL /api/member/logout/
# 전달 키값 : username, password1, password2, nickname
class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def saved_logout_log(self, user):
        log = ConnectedLog()
        log.user = user
        log.type = 'logout'
        log.ip_address = get_ip(self.request)
        log.user_agent = self.request.META['HTTP_USER_AGENT']
        return log.save()

    def post(self, request):
        response = Response({"detail": "Successfully logged out."},
                        status= status.HTTP_200_OK)

        self.saved_logout_log(self.request.user)
        response.delete_cookie('token')
        return response


# 1
# 회원가입 API
# URL /api/member/signup/
# 전달 키값 : username, password1, password2, nickname
class SignUp(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return HttpResponseRedirect(redirect_to='/okay/')
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return HttpResponseRedirect(redirect_to='/signup/')


# 1
# 페이스북 로그인 API
# URL /api/member/facebookLogin/
# 전달 키값 : token
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

        else:
            pass

        # 유저 시리얼라이즈 결과를 Response
        # token도 추가
        data = {
            'user': UserSerializer(user).data,
            'token': jwt_token_generator(user),
        }

        response = Response(data, status=status.HTTP_200_OK)
        if api_settings.JWT_AUTH_COOKIE:
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                response.data['token'],
                                max_age=21600,
                                httponly=True)
        return response


# 1
# 이메일 전달체킹 완료시 비밀번호변경 API
# URL /api/member/passwordReset/
class PasswordReset(APIView):
    permission_classes = (AllowAny, )

    def social_check(self, user):
        if user.user_type is not 'd':
            raise APIException('소셜계정은 비밀번호를 변경할수 없습니다.')
        return user

    def post(self, request, *args, **kwargs):

        uidb64 = self.request.data['uid']
        token = self.request.data['token']

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            self.social_check(user)

            data = {
                "password1": self.request.data['password1'],
                "password2": self.request.data['password2']

            }

            serializer = ChangePasswordSerializer(data=data)

            if serializer.is_valid():
                # Check old password

                # set_password also hashes the password that the user will get
                user.set_password(serializer.data['password1'])
                user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponseRedirect(redirect_to='/')


# 1
# 유저정보 관련 API
# URL /api/member/userInfo/
class UserInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = self.request.user
        serializer = UserSerializer(user)
        if user.is_authenticated:
            try:
                profile_image = ProfileImage.objects.select_related('user').filter(user=user).get()
                profile_serializer = ProfileImageSerializer(profile_image)

                if serializer:
                    return Response({"user": serializer.data,
                                     "profileImg": profile_serializer.data},
                                    status=status.HTTP_200_OK)
                return Response({"detail": "NO User"})

            except ObjectDoesNotExist:
                return Response({"user": serializer.data,
                                 "profileImg": {
                                     "profile_image": 'https://devtestserver.s3.amazonaws.com/media/example/2_x20_.jpeg',
                                     "cover_image": 'https://devtestserver.s3.amazonaws.com/media/example/1.jpeg'
                                 }}, status=status.HTTP_200_OK)

        else:
            response = Response(
                {
                    "code": 402,
                    "message": kr_error_code(402)
                }
                , status=status.HTTP_402_PAYMENT_REQUIRED)
            response.delete_cookie('token')

            return response


# 1
# 초대메일 API
# URL /api/member/invite/
# 데이터 전송 키 값 : email
class SendInviteEmail(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = self.request.data

        user = InviteUser.objects.create(email=data['email'])
        task = InviteUserTask
        email = task.delay(user.pk, self.request.user.pk)
        if email:
            return Response({"detail": "Email Send Success"}, status=status.HTTP_200_OK)
        raise APIException({"Email send failed"})


# 1
# 패스워드 분실시 비밀번호 초기화 API
# URL /api/member/passwordResetEmail/
# 데이터 전송 키 값 : username
class PasswordResetSendEmail(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = self.request.data

        try:
            user = User.objects.filter(username=data['username']).get()
            task = PasswordResetTask

            email = task.delay(user.pk)

            if email:
                return Response({"detail": "Email Send Success"}, status=status.HTTP_200_OK)
            raise APIException({"Email send failed"})
        except ObjectDoesNotExist:
            raise APIException({"this username is not valid"})


# 1
# 초대 DB에 쌓는 API
# URL /api/member/secondInvite/
# 데이터 전송 키 값 : email

class InvitationUserView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        data = self.request.data

        if InvitationUser.objects.create(email=data['email']):
            return Response({"detail": "sucess"}, status=status.HTTP_200_OK)
        return Response({"detail": "fail"}, status=status.HTTP_400_BAD_REQUEST)



