from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Post
from member.models import User, PointHistory,BuyList


__all__ = (
    'PostBuy',
)


class PostBuy(APIView):

    # 구매리스트에 존재하는지 판명
    def buylist_duplicate(self,post):
        buylist = BuyList.objects.filter(user=self.request.user, post_id=post.id)
        if len(buylist) is not None:
            raise exceptions.APIException({"detail":"It's a post I've already purchased"}, 400)
        return BuyList.objects.filter(user=self.request.user).create(post_id=post.id)

    def post(self,request):
        data = self.request.data
        if not self.request.user.is_authenticated:
            raise exceptions.NotAuthenticated()

        user_queryset = User.objects.filter(id=self.request.user.id).get()
        post_queryset = Post.objects.filter(id=data['post_id']).get()

        # 포인트가 적을시에 오류 발생
        if post_queryset.price > user_queryset.point:
            raise exceptions.APIException({"detail": "There is not enough points."}, 400)

        # 구매한 기록이 있는지를 확인
        if self.buylist_duplicate(post_queryset):
            if PointHistory.objects.filter(user=self.request.user, post_id=post_queryset.id) is not None:
                raise exceptions.APIException({"detail": "Failed insert PointHistory."}, 400)

            # 구매내역에 추가
            PointHistory.objects.buy(user=self.request.user, point=post_queryset.price,
                                     history=post_queryset.title)

            BuyList.objects.get_or_create(user=self.request.user, post_id=post_queryset.id)
            # 유저 포인트 업데이트
            user_queryset.point -= post_queryset.price
            user_queryset.save()

            # 구매횟수 증가
            post_queryset.buy_count += 1
            post_queryset.save()

            return Response({"detail": "Success buy."}, status=status.HTTP_200_OK)

        raise exceptions.APIException({"detail": "Failed buy."}, 400)


