import json

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import Profile, PayList
from utils.error_code import kr_error_code
from utils.pay_check import BootpayApi

__all__ = (
    'ShopUserData',
    'BootPayCheckView'
)


class BootPayCheckView(APIView):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.data

        # api = BootpayApi("5ab88457b6d49c1aaa550daa", "ja0mQQI+zwpS2YlCqoJuqBXsfPcVfzUlSDLRMigalDg=")
        #
        # text = api.confirm(data['receipt_id']).text
        # json_data = json.loads(text)
        #
        # if json_data['data']['status'] is 1:
        #     if json_data['data']['method'] is 'card':
        #         PayList.objects.card(user=user, price=json_data['data']['price'], content=json_data['data']['price'])
        #         return Response({1}, status=status.HTTP_200_OK)
        #     elif json_data['data']['method'] is 'phone':
        #         PayList.objects.phone(user=user, price=json_data['data']['price'], content=json_data['data']['price'])
        #         return Response({1}, status=status.HTTP_200_OK)
        #     return Response({2}, status=status.HTTP_200_OK)
        #
        # elif json_data['data']['status'] is 0 or 2 or 3:
        #     return Response({3}, status=status.HTTP_200_OK)

        pay = PayList.objects.create(user=user, price=data['price'],
                                     content=data['price'],
                                     payment_type=None,
                                     order_num=data['receipt_id'])
        user.point += int(data['price'])
        user.save()
        if pay:
            return Response({"detail": user.point}, status=status.HTTP_200_OK)
        return Response(
            {
                "code": 425,
                "message": kr_error_code(425)
            }
            , status=status.HTTP_400_BAD_REQUEST)


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
            Profile.objects.create(user=user)

            return Response({"detail":
                {
                    "username": user.nickname,
                    "email": user.username,
                    "phone": " ",
                    "addr": " "
                }
            }, status=status.HTTP_200_OK)
