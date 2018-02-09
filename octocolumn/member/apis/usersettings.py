from rest_framework import exceptions, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import UserSecondPassword, User
from member.serializers import SecondPasswordSerializer

__all__ =(
    'SecondPasswordCreateView',
    'ValidationSecondPassword'
)


class SecondPasswordCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SecondPasswordSerializer
    queryset = UserSecondPassword.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return User.objects.filter(user=self.request.user)
        else:
            raise exceptions.NotAuthenticated()

    def validated_password(self, data):
        second_password = data
        if type(second_password) is not int:
            raise exceptions.ValidationError('숫자만 입력이 가능합니다.')

        if len(second_password) is not 4:
            raise exceptions.ValidationError('패스워드는 4자리르 입력하셔야합니다.')
        return data

    def post(self, request, *args, **kwargs):
        user = self.request.user
        numeric_password = self.validated_password(self.request.data['second_password'])

        serializer = SecondPasswordSerializer(super().get_queryset().get_or_create(user=user, second_password=numeric_password))

        if serializer:
            return Response({"detail": serializer.validated_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Already added."}, status=status.HTTP_200_OK)


class ValidationSecondPassword(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SecondPasswordSerializer
    queryset = UserSecondPassword.objects.all()

    def post(self, request):
        user = self.request.user
        numeric_password = self.request.data['second_password']

        user_data = UserSecondPassword.objects.filter(user=user)

        if user_data.error_count >= 5:
            return Response({"detail": "The number of errors exceeded"}, status=status.HTTP_401_UNAUTHORIZED)

        if numeric_password is not user_data.second_password:
            UserSecondPassword.objects.filter(user=user).increase()
        return Response({"detail": "Success Credential"}, status=status.HTTP_200_OK)


