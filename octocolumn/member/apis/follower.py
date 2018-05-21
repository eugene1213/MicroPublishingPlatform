from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, exceptions
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Post
from member.models import User, ProfileImage, Profile
from member.models.user import Relation, Bookmark
from member.serializers import ProfileImageSerializer, ProfileMainSerializer, FollowStatusSerializer
from utils.error_code import kr_error_code

__all__ = (
    'Follower',
    'Waiting',
    'BookmarkView',
    'GetUserFollowingCard',
    'GetUserFollowerCard',
    'FollowerStatus'
)


class FollowerStatus(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user_pk = self.kwargs.get('user_pk')

        user = self.request.user

        try:
            to_user = User.objects.filter(pk=user_pk).get()
            serializer = FollowStatusSerializer(to_user, context={'request': request})
            if serializer:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {
                    "code": 500,
                    "message": kr_error_code(500)
                }
                , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ObjectDoesNotExist:
            return Response(
                {
                    "code": 500,
                    "message": kr_error_code(500)
                }
                , status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# 1
# 팔로워 API
# URL  /api/member/(?P<user_pk>\d+)/follow/$
class Follower(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request, *args, **kwargs):
        user = self.request.user
        user_pk = self.kwargs.get('user_pk')

        try:
            to_user = User.objects.filter(pk=user_pk).get()
            result, relation = Relation.objects.select_related('to_user', 'from_user').get_or_create(to_user=to_user, from_user=user)

            if relation:
                return Response({'detail': 'created',
                                 "author": {
                                     "follow_status": True,
                                     "follower": Relation.objects.select_related('from_user').filter(from_user=user).count()
                                 }
                                 })
            result.delete()
            return Response({'detail': 'deleted',
                             "author": {
                                 "follow_status": False
                             }
                             })

        except ObjectDoesNotExist:
            return Response(
                {
                    "code": 500,
                    "message": kr_error_code(500)
                }
                , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 1
# 기다림 API
# URL  /api/member/(?P<user_pk>\d+)/waiting/$
class Waiting(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_pk = self.kwargs.get('user_pk')

        try:
            from_user = User.objects.filter(pk=user_pk).get()
            result = from_user.waiting_toggle(user)

            if result:
                return Response({'detail': 'created'})
            return Response({'created': 'deleted'})

        except ObjectDoesNotExist:
            return Response(
                {
                    "code": 500,
                    "message": kr_error_code(500)
                }
                , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 1
# 기다림 API
# URL  /api/member/(?P<book_pk>\d+)/bookmark/$
class BookmarkView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        post_pk = self.kwargs.get('post_pk')
        user = self.request.user

        try:
            post = Post.objects.filter(pk=post_pk).get()
            result, relation = Bookmark.objects.get_or_create(user=user, post=post)
            if relation:
                return Response({'detail': 'created'})
            result.delete()
            return Response({'created': 'deleted'})

        except ObjectDoesNotExist:
            return Response(
                {
                    "code": 500,
                    "message": kr_error_code(500)
                }
                , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 1
# 내가 팔로워 하고있는 유저를 프로필에 유저정보카드를 리스트화 시켜서 내보내는 함수 (from_user== 나  , to_user 상대)
# URL /api/member/getUserFollowingCard/(?P<count>\w+)$
class GetUserFollowingCard(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        count = self.kwargs.get('count')
        if count != 0:
            # 내가 팔로워하는 유저
            follower = Relation.objects.filter(from_user=user)[int(count):int(count) + 4]

            if follower.count != 0:

                list = []
                for i in follower:
                    try:

                        profile = Profile.objects.filter(user=i.to_user).get()
                        profile_serializer = ProfileMainSerializer(profile)

                        data = {
                                "pk": i.to_user.id,
                                "follower": Relation.objects.filter(to_user=i.to_user).count(),
                                "nickname": i.to_user.nickname,
                                "intro": profile_serializer.data['intro'],
                                "profile_img": profile_serializer.data['image']['profile_image'],
                                "cover_img": profile_serializer.data['image']['cover_image']

                        }

                        list.append(data)
                        pass

                    except ObjectDoesNotExist:
                            try:
                                profile_image = ProfileImage.objects.filter(user=i.to_user).get()

                                serializer = ProfileImageSerializer(profile_image)

                                if serializer:
                                    data = {
                                        "pk": i.to_user.id,
                                        "follower": Relation.objects.filter(to_user=i.to_user).count(),
                                        "nickname": i.to_user.nickname,
                                        "intro": '-',
                                        "profile_img": serializer.data['profile_image'],
                                        "cover_img": serializer.data['cover_image']

                                    }
                                    list.append(data)
                                    pass
                                return Response(
                                    {
                                        "code": 500,
                                        "message": kr_error_code(500)
                                    }
                                    , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            except ObjectDoesNotExist:

                                    data = {
                                        "pk": i.to_user.id,
                                        "follower": Relation.objects.filter(to_user=i.to_user).count(),
                                        "nickname": i.to_user.nickname,
                                        "intro": '-',
                                        "profile_img": 'https://static.octocolumn.com/media/example/2_x20_.jpeg',
                                        "cover_img": 'https://static.octocolumn.com/media/example/1.jpeg'

                                    }
                                    list.append(data)
                                    pass
                return Response(list, status=status.HTTP_200_OK)

            else:
                return Response({}, status=status.HTTP_200_OK)

        else:
            follower = Relation.objects.filter(from_user=user)[0:4].all()

            if follower.count != 0:

                list = []
                for i in follower:
                    try:

                        profile = Profile.objects.filter(user=i.to_user).get()
                        profile_serializer = ProfileMainSerializer(profile)

                        data = {
                                "pk": i.to_user.id,
                                "follower": Relation.objects.filter(to_user=i.to_user).count(),
                                "nickname": i.to_user.nickname,
                                "intro": profile_serializer.data['intro'],
                                "profile_img": profile_serializer.data['image']['profile_image'],
                                "cover_img": profile_serializer.data['image']['cover_image']

                        }

                        list.append(data)
                        pass

                    except ObjectDoesNotExist:
                            try:
                                profile_image = ProfileImage.objects.filter(user=i.to_user).get()

                                serializer = ProfileImageSerializer(profile_image)

                                if serializer:
                                    data = {
                                        "pk": i.to_user.id,
                                        "follower": Relation.objects.filter(to_user=i.to_user).count(),
                                        "nickname": i.to_user.nickname,
                                        "intro": '-',
                                        "profile_img": serializer.data['profile_image'],
                                        "cover_img": serializer.data['cover_image']

                                    }
                                    list.append(data)
                                    pass
                                return Response(
                                    {
                                        "code": 500,
                                        "message": kr_error_code(500)
                                    }
                                    , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            except ObjectDoesNotExist:

                                    data = {
                                        "pk": i.to_user.id,
                                        "follower": Relation.objects.filter(to_user=i.to_user).count(),
                                        "nickname": i.to_user.nickname,
                                        "intro": '-',
                                        "profile_img": 'https://static.octocolumn.com/media/example/2_x20_.jpeg',
                                        "cover_img": 'https://static.octocolumn.com/media/example/1.jpeg'

                                    }
                                    list.append(data)
                                    pass
                return Response(list, status=status.HTTP_200_OK)

            else:
                return Response({}, status=status.HTTP_200_OK)
            # return Response({},200)


# 1
# 나를 팔로우 하고있는 유저를 프로필에 유저정보카드를 리스트화 시켜서 내보내는 함수 (to_user가 나   , from_user 상대)
# URL /api/member/getUserFollowerCard/(?P<count>\w+)$
class GetUserFollowerCard(ListAPIView):
    permission_classes = (IsAuthenticated,)

    # 팔로우 상태를 검사하는
    def follower_status(self, user):
        try:
            Relation.objects.filter(to_user=self.request.user, from_user=user).get()
            return True
        except ObjectDoesNotExist:
            return False

    def get(self, request, *args, **kwargs):
        user = self.request.user
        count = self.kwargs.get('count')
        if count != 0:

            follower = Relation.objects.filter(to_user=user)[int(count):int(count)+4]
            if follower.count() != 0:

                list = []
                for i in follower:
                    try:

                        profile = Profile.objects.filter(user=i.from_user).get()
                        profile_serializer = ProfileMainSerializer(profile)

                        data = {
                                "pk": i.from_user.id,
                                "follower": Relation.objects.filter(from_user=i.from_user).count(),
                                "nickname": i.from_user.nickname,
                                "follow_status": self.follower_status(i.from_user),
                                "intro": profile_serializer.data['intro'],
                                "profile_img": profile_serializer.data['image']['profile_image'],
                                "cover_img": profile_serializer.data['image']['cover_image']

                        }

                        list.append(data)
                        pass
                    except ObjectDoesNotExist:
                            try:
                                profile_image = ProfileImage.objects.filter(user=i.from_user).get()

                                serializer = ProfileImageSerializer(profile_image)

                                if serializer:
                                    data = {
                                        "pk": i.from_user.id,
                                        "follower": Relation.objects.filter(from_user=i.from_user).count(),
                                        "nickname": i.from_user.nickname,
                                        "follow_status": self.follower_status(i.from_user),
                                        "intro": '-',
                                        "profile_img": serializer.data['profile_image'],
                                        "cover_img": serializer.data['cover_image']

                                    }
                                    list.append(data)
                                    pass
                                return Response(
                                    {
                                        "code": 500,
                                        "message": kr_error_code(500)
                                    }
                                    , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            except ObjectDoesNotExist:

                                    data = {
                                        "pk": i.from_user.id,
                                        "follower": Relation.objects.filter(from_user=i.from_user).count(),
                                        "nickname": i.from_user.nickname,
                                        "follow_status": self.follower_status(i.from_user),
                                        "intro": '-',
                                        "profile_img": 'https://static.octocolumn.com/media/example/2_x20_.jpeg',
                                        "cover_img": 'https://static.octocolumn.com/media/example/1.jpeg'

                                    }
                                    list.append(data)
                                    pass

                return Response(list, status=status.HTTP_200_OK)

            else:
                return Response({}, status=status.HTTP_200_OK)

        else:
            follower = Relation.objects.filter(to_user=user)[0:4].get()

            if follower.count() != 0:

                list = []
                for i in follower:
                    try:

                        profile = Profile.objects.filter(user=i.from_user).get()
                        profile_serializer = ProfileMainSerializer(profile)

                        data = {
                            "pk": i.from_user.id,
                            "follower": Relation.objects.filter(from_user=i.from_user).count(),
                            "nickname": i.from_user.nickname,
                            "follow_status": self.follower_status(i.from_user),
                            "intro": profile_serializer.data['intro'],
                            "profile_img": profile_serializer.data['image']['profile_image'],
                            "cover_img": profile_serializer.data['image']['cover_image']

                        }

                        list.append(data)
                        pass
                    except ObjectDoesNotExist:
                        try:
                            profile_image = ProfileImage.objects.filter(user=i.from_user).get()

                            serializer = ProfileImageSerializer(profile_image)

                            if serializer:
                                data = {
                                    "pk": i.from_user.id,
                                    "follower": Relation.objects.filter(from_user=i.from_user).count(),
                                    "nickname": i.from_user.nickname,
                                    "follow_status": self.follower_status(i.from_user),
                                    "intro": '-',
                                    "profile_img": serializer.data['profile_image'],
                                    "cover_img": serializer.data['cover_image']

                                }
                                list.append(data)
                                pass
                            return Response(
                                {
                                    "code": 500,
                                    "message": kr_error_code(500)
                                }
                                , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        except ObjectDoesNotExist:

                            data = {
                                "pk": i.from_user.id,
                                "follower": Relation.objects.filter(from_user=i.from_user).count(),
                                "nickname": i.from_user.nickname,
                                "follow_status": self.follower_status(i.from_user),
                                "intro": '-',
                                "profile_img": 'https://static.octocolumn.com/media/example/2_x20_.jpeg',
                                "cover_img": 'https://static.octocolumn.com/media/example/1.jpeg'

                            }
                            list.append(data)
                            pass

                return Response(list, status=status.HTTP_200_OK)

            else:
                return Response({}, status=status.HTTP_200_OK)



