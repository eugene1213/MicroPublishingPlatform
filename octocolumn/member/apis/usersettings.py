from django.contrib.auth.hashers import make_password, check_password
from rest_framework import exceptions, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import User, OtherPassword
from member.serializers import SecondPasswordSerializer

__all__ =(
    'SecondPasswordCreateView',
    'ValidationSecondPassword'
)


class SecondPasswordCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SecondPasswordSerializer
    queryset = OtherPassword.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return User.objects.filter(user=self.request.user)
        else:
            raise exceptions.NotAuthenticated()

    def validate_password(self, data):
        second_password = data

        if int(second_password) is not int:
            raise exceptions.ValidationError({"detail":'패스워드는 숫자만 입력하셔야 합니다.'})

        if len(second_password) is not 4:
            raise exceptions.ValidationError({"detail":'패스워드는 4자리만 입력하셔야 합니다.'})
        return data

    def post(self, request, *args, **kwargs):
        user = self.request.user
        numeric_password = self.validate_password(self.request.data['second_password'])
        password = make_password(numeric_password, None, 'PBKDF2')

        serializer = SecondPasswordSerializer(OtherPassword.objects.create(user=user, second_password=password))

        if serializer:
            return Response({"detail": serializer.validated_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Already added."}, status=status.HTTP_200_OK)


class ValidationSecondPassword(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SecondPasswordSerializer
    queryset = OtherPassword.objects.all()

    def post(self, request):
        user = self.request.user
        numeric_password = self.request.data['second_password']

        user_data = OtherPassword.objects.filter(user=user)

        if user_data.error_count >= 5:
            return Response({"detail": "The number of errors exceeded"}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(numeric_password, user_data.second_password):
            OtherPassword.objects.increase(user=user)
            return Response({"detail": "Failed Credential"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"detail": "Success Credential"}, status=status.HTTP_200_OK)


