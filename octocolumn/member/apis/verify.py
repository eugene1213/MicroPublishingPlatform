from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from member.models import User, Profile, ProfileImage
from member.serializers import UserSerializer
from utils.jwt import jwt_token_generator
from utils.tokengenerator import account_activation_token

__all__ = (
    'VerifyEmail',
    'InviteVerifyEmail',
    'PasswordResetEmail'
)


class VerifyEmail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            Profile.objects.create(user=user)
            ProfileImage.objects.create(user=user)
            user.is_active = True
            user.save()
            return HttpResponseRedirect(redirect_to='/')
        else:
            return Response('Activation link is invalid!', status=404)


class InviteVerifyEmail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            return HttpResponseRedirect(redirect_to='/signinForm/')
        else:
            return Response('Activation link is invalid!', status=404)


# 1

class PasswordResetEmail(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):

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
        else:
            return Response('Activation link is invalid!', status=404)