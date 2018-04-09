from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import User, OctoCode
from member.serializers import OctoCodeSerializer

__all__ =(
    'OctoCodeView',
)


class OctoCodeView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OctoCodeSerializer
    queryset = OctoCode.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return User.objects.filter(user=self.request.user)
        else:
            raise exceptions.NotAuthenticated()

    def validate_code(self, data):

        # 형태가 integer인지 체크
        try:
            code = int(data)

        except ValueError:
            raise exceptions.ValidationError({"detail": 'password is only numeric character'})

        if len(data) is not 4:
            raise exceptions.ValidationError({"detail": 'password is only 4 character'})
        return data

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.data['code']

        try:
            octo_code = OctoCode.objects.filter(user=user).get().octo_code

        except ObjectDoesNotExist:
            raise exceptions.ValidationError({"detail": "This account does not have octo_code"})

        code = self.validate_code(data)

        if code == octo_code:
            return Response({"detail": True}, status=status.HTTP_202_ACCEPTED)
        raise exceptions.AuthenticationFailed({"detail": "OctoCode is not valid"})

    def put(self, request,*args, **kwargs):
        user = self.request.user
        data = self.request.data['code']

        try:
            octo_code = OctoCode.objects.filter(user=user).get().octo_code
            raise exceptions.ValidationError({"detail": "Already Exist code"})
        except ObjectDoesNotExist:
            pass

        code = self.validate_code(data)

        if code:
            if OctoCode.objects.create(user=user, octo_code=code):
                return Response({"detail": True}, status=status.HTTP_201_CREATED)







