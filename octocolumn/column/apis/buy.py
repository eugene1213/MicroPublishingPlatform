from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Post
from member.models import  User, PointHistory
from member.models.user import BuyList

__all__ = (
    'PostBuy',
)


class PostBuy(APIView):
    # point 감소 로직
    def decrease_point(self,point):
        return User.objects.filter(user=self.request.user).decrease_point(point=point)

    # 구매리스트에 존재하는지 판명
    def buylist_duplicate(self,post):
        buylist = BuyList.objects.filter(user=self.request.user, post_id=post.id).get()
        if buylist is not None:
            return Response({"detail":"It's a post I've already purchased"} , status=status.HTTP_400_BAD_REQUEST)
        return BuyList.objects.get_or_create(user=self.request.user, post_id=post.id)

    # 구매시 카운트 증가 로직
    def increase_buy_count(self,post_id):
        return Post.objects.filter(id=post_id).increase_buy_count()

    def post(self,request):
        data = self.request.data
        if not self.request.user.is_authenticated:
            raise exceptions.NotAuthenticated()

        user_queryset = User.objects.filter(username=self.request.user).get()
        post_queryset = Post.objects.filter(id=data['post_pk']).get()
        if post_queryset.price > user_queryset.point:
            raise Response({"detail":"There is not enough points."} , status=status.HTTP_400_BAD_REQUEST)

        if self.buylist_duplicate(post_queryset):
            PointHistory.objects.get_or_create(user=self.request.user,point_use_type='b',point=post_queryset.price,
                                              history=post_queryset.title)
            self.decrease_point(post_queryset.price)
            self.increase_buy_count(data['post_id'])

            return Response({"detail": "Success buy."}, status=status.HTTP_200_OK)

        return Response({"detail": "Failed buy."}, status=status.HTTP_400_BAD_REQUEST)


