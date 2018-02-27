from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import User

__all__ = (
    'Follower',
)


class Follower(APIView):
    def post(self, request):
        user = self.request.user
        data = self.request.data
        to_user = User.objects.filter(pk=data['user_id']).get()
        from_user = User.objects.filter(pk=user.pk).get()
        from_user.save()
        from_user.follow_toggle(to_user)

        return Response({"detail":"success"}, status=status.HTTP_200_OK)
