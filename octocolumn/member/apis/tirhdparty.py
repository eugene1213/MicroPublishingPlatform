
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from typing import NamedTuple
from rest_framework.response import Response


from config.settings import CLIENT_ID
from member.backends import GoogleBackend
from member.models import User
from member.serializers import UserSerializer
from utils.jwt import jwt_token_generator

__all__ =(
    'GoogleLogin',
)


class GoogleLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = self.request.data

        class DebugTokenInfo(NamedTuple):
            aud: str
            azp: str
            sub: str
            email: str
            email_verified: bool
            at_hash: str
            exp: int
            iss: str
            jti: str
            iat: int
            name: str
            picture: str
            given_name: str
            family_name: str
            locale: str

        def get_debug_token_info(token):
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
            return DebugTokenInfo(**idinfo)

        debug_token_info = get_debug_token_info(request.data['access_token'])

        if debug_token_info.iss not in ['accounts.google.com', 'https://accounts.google.com']:
            raise APIException('페이스북 토큰의 사용자와 전달받은 facebook_user_id가 일치하지 않음')

        if not debug_token_info.email_verified:
            raise APIException('페이스북 토큰이 유효하지 않음')

        user_id = debug_token_info.sub

        userinfo = User.objects.filter(username=debug_token_info.email).count()

        if not userinfo == 0:
            raise APIException('Already exists this email')

        user = GoogleBackend.authenticate(google_user_id=user_id)

        if not user:
            user = User.objects.create_google_user(
                username=debug_token_info.email,
                first_name=debug_token_info.given_name,
                last_name=debug_token_info.family_name,
                social_id=f'g_{user_id}',
            )


        data = {
            'user': UserSerializer(user).data,
            'token': jwt_token_generator(user)
        }
        return Response(data)
