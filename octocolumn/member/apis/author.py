from rest_framework import generics, mixins, exceptions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from member.models import Author as AuthorModel, User
from member.serializers import AuthorSerializer


class AuthorAplly(generics.GenericAPIView,
             mixins.ListModelMixin,
             mixins.CreateModelMixin,
             mixins.DestroyModelMixin):
    permission_classes = (IsAuthenticated, )
    queryset = AuthorModel.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return User.objects.filter(username=self.request.user)
        else:
            raise exceptions.NotAuthenticated()

    #작가 신청메서드
    def post(self, request):
        user = self.request.user
        data = self.request.data

        author, result = super().get_queryset().get_or_create(author=user, intro=data['intro'], blog=data['blog'])

        if result:
            return Response({"detail":"Successfully added."}, status=status.HTTP_201_CREATED)
        else:
            raise exceptions.APIException({"detail":"Already added."}, 200)


