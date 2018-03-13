from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import User

__all__ = (
    'Follower',
    'Waiting'
)


class Follower(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request, *args, **kwargs):
        user = self.request.user
        user_pk = self.kwargs.get('user_pk')

        try:
            from_user = User.objects.filter(pk=user_pk).get()
            result = from_user.follow_toggle(user)

            if result:
                from_user.following_users_count += 1
                user.follower_users_count += 1
                user.save()
                from_user.save()
                return Response({'detail': 'created'})
            from_user.following_users_count -= 1
            user.follower_users_count -= 1
            user.save()
            from_user.save()
            return Response({'created': 'deleted'})

        except ObjectDoesNotExist:
            raise exceptions.ValidationError({"detail": "Abnormal connected"})


class Waiting(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_pk = self.kwargs.get('user_pk')

        try:
            from_user = User.objects.filter(pk=user_pk).get()
            result = from_user.waiting_toggle(user)

            if result:
                from_user.waiting_count += 1
                from_user.save()
                return Response({'detail': 'created'})
            from_user.waiting_count -= 1
            from_user.save()
            return Response({'created': 'deleted'})

        except ObjectDoesNotExist:
            raise exceptions.ValidationError({"detail": "Abnormal connected"})

