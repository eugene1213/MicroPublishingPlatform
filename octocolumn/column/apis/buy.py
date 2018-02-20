from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Post
from member.models import User, PointHistory,BuyList


__all__ = (
    'PostBuy',
)


class PostBuy(APIView):
    # point 감소 로직
    def decrease_point(self, point):
        return User.objects.filter(id=self.request.user.id).update(point=point)

    # 구매리스트에 존재하는지 판명
    def buylist_duplicate(self,post):
        buylist = BuyList.objects.filter(user=self.request.user, post_id=post.id)
        if len(buylist) is not None:
            raise exceptions.APIException({"detail":"It's a post I've already purchased"}, 400)
        return BuyList.objects.filter(user=self.request.user).create(post_id=post.id)

    # 구매시 카운트 증가 로직
    def increase_buy_count(self,post_id):
        return Post.objects.filter(id=post_id).increase_buy_count()

    def post(self,request):
        data = self.request.data
        if not self.request.user.is_authenticated:
            raise exceptions.NotAuthenticated()

        user_queryset = User.objects.filter(id=self.request.user.id).get()
        post_queryset = Post.objects.filter(id=data['post_id']).get()

        if post_queryset.price > user_queryset.point:
            raise exceptions.APIException({"detail":"There is not enough points."}, 400)

        if self.buylist_duplicate(post_queryset):
            if PointHistory.objects.filter(user=self.request.user, post_id=post_queryset.id) is not None:
                raise exceptions.APIException({"detail": "Failed insert PointHistory."}, 400)

            PointHistory.objects.buy(user=self.request.user, point=post_queryset.price,
                                              history=post_queryset.title)

            BuyList.objects.get_or_create(user=self.request.user, post_id=post_queryset.id)
            self.decrease_point(user_queryset.point-post_queryset.price)
            self.increase_buy_count(data['post_id'])

            return Response({"detail": "Success buy."}, status=status.HTTP_200_OK)

        raise exceptions.APIException({"detail": "Failed buy."}, 400)


