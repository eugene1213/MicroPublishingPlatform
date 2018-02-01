from rest_framework import exceptions, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from member.models import UserSecondPassword, User
from member.serializers import SecondPasswordSerializer


class CreateSecondPassword(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SecondPasswordSerializer
    queryset = UserSecondPassword.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return User.objects.filter(user=self.request.user)
        else:
            raise exceptions.NotAuthenticated()

    def post(self, request):
        user = self.request.user
        second_password = self.request.data['second_password']
        second, result = super().get_queryset().get_or_create(user=user, second_password=second_password)

        if result:
            return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Already added."}, status=status.HTTP_200_OK)

