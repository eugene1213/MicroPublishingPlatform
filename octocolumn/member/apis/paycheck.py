from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import Profile
from utils.pay_check import BootpayApi

__all__ = (
    'ShopUserData',
)


# class BootPayCheckView(APIView):
#     def post(self, request, *args, **kwargs):
#         data = self.request.data
#
#         api = BootpayApi("5ab88457b6d49c1aaa550daa", rec)
#
#         return Response({
#             api.confirm(data['receipt_id']).text
#         }, status=status.HTTP_200_OK)
#

class ShopUserData(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        try:
            profile = Profile.objects.filter(user=user).get()
            if profile.phone is None:
                return Response({"detail":
                    {
                        "username": user.nickname,
                        "email": user.username,
                        "phone": " ",
                        "addr": " "
                    }
                }, status=status.HTTP_200_OK)
            return Response({"detail":
                {
                    "username": user.nickname,
                    "email": user.username,
                    "phone": profile.phone,
                    "addr": " "

                }
            }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            profile = Profile.objects.create(user=user)

            return Response({"detail":
                {
                    "username": user.nickname,
                    "email": user.username,
                    "phone": " ",
                    "addr": " "
                }
            }, status=status.HTTP_200_OK)
