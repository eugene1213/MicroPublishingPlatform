from datetime import datetime
from random import randint

from django.utils.dateformat import DateFormat
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import SearchTag, Tag
from member.models import Profile


__all__ = (
    'PaymentInfo',
)


class PaymentInfo(APIView):
    def post(self, request, *args, **kwargs):
        user = self.request.user

        if user.is_authenticated:
            profile = Profile.objects.filter(user=user).get()
            order_number = str(DateFormat(datetime.now()).format('Ymd')) + str(user.pk) + str(randint(1000, 9999))

            return Response({
                "detail":
                    {
                        "email": user.username,
                        "username": user.nickname,
                        "phone": profile.phone,
                        "order_num": order_number

                    }
            }, status=status.HTTP_200_OK)


# class Test(APIView):
#     def post(self, request, *args, **kwargs):
#         search_tag = SearchTag.objects.all()
#
#         for i in search_tag:
#             tags = Tag.objects.create(tags=i.tag)
#             i.post.tags.add(tags)
#
#         return Response({
#             "success"
#         }, status=status.HTTP_200_OK)