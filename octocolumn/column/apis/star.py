from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from column.models import Post
from column.models.star import PostStar
from utils.error_code import kr_error_code

__all__ = (
    'Star',
)


class Star(generics.GenericAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        user = self.request.user
        data = self.request.data
        post = Post.objects.filter(pk=data['pk']).get()

        if isinstance(data['star'], int):
            if data['star'] >= 0 or data['star'] <= 10:
                try:
                    buy_list = user.buy_list.filter(post=post).get()
                    if not buy_list.star:
                        star = PostStar.objects.filter(post=post).get()
                        star.content += data['star']
                        star.member_num += 1
                        buy_list.star = True
                        buy_list.save()
                        star.save()
                        return Response(
                        )
                    return Response(
                        {
                            "code": 402,
                            "message": kr_error_code(402)
                        }
                        , status=status.HTTP_402_PAYMENT_REQUIRED
                    )
                except ObjectDoesNotExist:
                    return Response(
                        {
                            "code": 402,
                            "message": kr_error_code(402)
                        }
                        , status=status.HTTP_402_PAYMENT_REQUIRED
                    )
            return Response(
                {
                    "code": 402,
                    "message": kr_error_code(402)
                }
                , status=status.HTTP_402_PAYMENT_REQUIRED
            )
        return Response(
            {
                "code": 402,
                "message": kr_error_code(402)
            }
            , status=status.HTTP_402_PAYMENT_REQUIRED
        )




