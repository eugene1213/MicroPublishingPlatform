from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Post
from member.models import Point, BuyList, User

__all__ = (
    'PostBuy',
)


class PostBuy(APIView):
    # point 감소 로직
    def decrease_point(self,point):
        return Point.objects.filter(user=self.request.user).update(point=self.request.user.point-point)

    # 구매리스트에 존재하는지 판명
    def buylist_duplicate(self,post):
        buylist = BuyList.objects.filter(user=self.request.user,post=post).get()
        if buylist is not None:
            return Response({"detail":"It's a post I've already purchased"} , status=status.HTTP_400_BAD_REQUEST)
        return BuyList.objects.get_or_create(user=self.request.user,post=post)

    def post(self,request):
        data = self.request.data
        if not self.request.user.is_authenticated:
            raise exceptions.NotAuthenticated()

        user_queryset = User.objects.filter(username=self.request.user).get()
        post_queryset = Post.objects.filter(id=data['post_pk']).get()

        if post_queryset.price > user_queryset.point:
            raise Response({"detail":"There is not enough points."} , status=status.HTTP_400_BAD_REQUEST)

        self.decrease_point(post_queryset.price)
        if self.buylist_duplicate(post_queryset):
            Point.objects.get_or_create(user=self.request.user,point_use_type='b',point=post_queryset.price,
                                              history=post_queryset.title)
            return Response({"detail": "Success buy."}, status=status.HTTP_200_OK)

        return Response({"detail": "Failed buy."}, status=status.HTTP_400_BAD_REQUEST)


