from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import User

__all__ = (
    'Follower',
)


class Follower(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        data = self.request.data
        try:
            to_user = User.objects.filter(pk=data['user_id']).get()
            from_user = User.objects.filter(pk=user.pk).get()
            result = from_user.follow_toggle(to_user)

            if result:
                return Response({'detail': 'created'})
            return Response({'created': 'deleted'})

        except ObjectDoesNotExist:
            raise exceptions.ValidationError({"detail": "Abnormal connected"})


