from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Post
from column.models.star import PostStar
from utils.error_code import kr_error_code

__all__ = (
    'Star',
)


class Star(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = self.request.user
        data = self.request.data
        post = Post.objects.filter(pk=data['pk']).get()

        if isinstance(int(data['star']), int):
            if data['star'] >= 0 or data['star'] <= 10:
                try:
                    buy_list = user.buy_list.filter(post=post).get()
                    if not buy_list.star:
                        star = PostStar.objects.filter(post=post).get()
                        star.content += int(data['star'])
                        star.member_num += 1
                        buy_list.star = True
                        buy_list.save()
                        star.save()
                        return Response(
                        )
                    return Response(
                        {
                            "code": 431,
                            "message": kr_error_code(431)
                        }
                        , status=status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
                    )
                except ObjectDoesNotExist:
                    return Response(
                        {
                            "code": 407,
                            "message": kr_error_code(407)
                        }
                        , status=status.HTTP_402_PAYMENT_REQUIRED
                    )
            return Response(
                {
                    "code": 424,
                    "message": kr_error_code(424)
                }
                , status=status.HTTP_424_FAILED_DEPENDENCY
            )
        return Response(
            {
                "code": 424,
                "message": kr_error_code(424)
            }
            , status=status.HTTP_424_FAILED_DEPENDENCY
        )


class StarView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        data = self.request.data
        post = Post.objects.filter(pk=data['pk']).get()

        star = PostStar.objects.filter(post=post).get()

        return Response(
            {
                "detail":
                    {
                        "star": round(star.content/star.member_num)
                    }
            }
        )




