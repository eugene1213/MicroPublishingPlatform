from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, exceptions
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import User, ProfileImage, Profile
from member.models.user import Relation
from member.serializers import ProfileImageSerializer, ProfileSerializer

__all__ = (
    'Follower',
    'Waiting',
    'GetUserFollowingCard',
    'GetUserFollowerCard'
)


class Follower(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request, *args, **kwargs):
        user = self.request.user
        user_pk = self.kwargs.get('user_pk')

        try:
            from_user = User.objects.filter(pk=user_pk).get()
            result = user.follow_toggle(from_user)

            if result:
                from_user.following_users_count += 1
                user.follower_users_count += 1
                user.save()
                from_user.save()
                return Response({'detail': 'created',
                                 "author":{
                                     "follow_status": True,
                                     "follower": from_user.following_users_count
                                 }
                                 })
            from_user.following_users_count -= 1
            user.follower_users_count -= 1
            user.save()
            from_user.save()
            return Response({'detail': 'deleted',
                             "author": {
                                 "follow_status": False
                             }
                             })

        except ObjectDoesNotExist:
            raise exceptions.ValidationError({"detail": "Abnormal connected"})


class Waiting(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_pk = self.kwargs.get('user_pk')

        try:
            from_user = User.objects.filter(pk=user_pk).get()
            result = from_user.waiting_toggle(user)

            if result:
                from_user.waiting_count += 1
                from_user.save()
                return Response({'detail': 'created'})
            from_user.waiting_count -= 1
            from_user.save()
            return Response({'created': 'deleted'})

        except ObjectDoesNotExist:
            raise exceptions.ValidationError({"detail": "Abnormal connected"})


class GetUserFollowingCard(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        count = self.kwargs.get('count')
        if count:

            follower = Relation.objects.filter(to_user=user)[int(count):int(count)+4]
            if follower.count() != 0:

                # follower = Relation.objects.filter(from_user=user).get()
                list = []
                for i in follower:
                    try:

                        profile = Profile.objects.filter(user=i.to_user).get()
                        profile_serializer = ProfileSerializer(profile)

                        data = {
                                "pk": i.to_user.id,
                                "follower": i.to_user.follower_users_count,
                                "nickname": i.to_user.nickname,
                                "intro": profile_serializer.data['intro'],
                                "profile_img": profile_serializer.data['image']['profile_image'],
                                "cover_img": profile_serializer.data['image']['cover_image']

                        }

                        list.append(data)

                        return Response(list, status=status.HTTP_200_OK)
                    except ObjectDoesNotExist:
                            try:
                                profile_image = ProfileImage.objects.filter(user=i.to_user).get()

                                serializer = ProfileImageSerializer(profile_image)

                                if serializer:
                                    data = {
                                        "pk": i.to_user.id,
                                        "follower": i.to_user.follower_users_count,
                                        "nickname": i.to_user.nickname,
                                        "intro": '-',
                                        "profile_img": serializer.data['profile_image'],
                                        "cover_img": serializer.data['cover_image']

                                    }
                                    list.append(data)
                                    return Response(list, status=status.HTTP_200_OK)
                                raise exceptions.ValidationError('Abnormal connected')
                            except ObjectDoesNotExist:

                                    data = {
                                        "pk": i.to_user.id,
                                        "follower": i.to_user.follower_users_count,
                                        "nickname": i.to_user.nickname,
                                        "intro": '-',
                                        "profile_img": '/static/images/example/2.jpeg',
                                        "cover_img": '/static/images/example/1.jpeg'

                                    }
                                    list.append(data)
                                    return Response(list, status=status.HTTP_200_OK)

            else:
                return Response({}, status=status.HTTP_200_OK)

        else:
            follower = Relation.objects.filter(to_user=user)[0:4].get()

            list = []

            for i in follower:
                try:
                    profile = Profile.objects.filter(user=i.to_user).get()
                    profile_serializer = ProfileSerializer(profile)

                    data = {
                            "follower": i.to_user.follower_users_count,
                            "nickname": i.to_user.nickname,
                            "intro": profile_serializer.data['intro'],
                            "profile_img": profile_serializer.data['image']['profile_image'],
                            "cover_img": profile_serializer.data['image']['cover_image']


                    }
                    list.append(data)

                    return Response(list, status=status.HTTP_200_OK)
                except ObjectDoesNotExist:
                    raise exceptions.ValidationError({"detail": "must Register Profile"})

            return Response({},200)


class GetUserFollowerCard(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        count = self.kwargs.get('count')
        if count:

            follower = Relation.objects.filter(from_user=user)[int(count):int(count)+4]
            if follower.count() != 0:

                # follower = Relation.objects.filter(from_user=user).get()
                list = []
                for i in follower:
                    try:

                        profile = Profile.objects.filter(user=i.to_user).get()
                        profile_serializer = ProfileSerializer(profile)

                        data = {
                                "pk": i.to_user.id,
                                "follower": i.to_user.follower_users_count,
                                "nickname": i.to_user.nickname,
                                "intro": profile_serializer.data['intro'],
                                "profile_img": profile_serializer.data['image']['profile_image'],
                                "cover_img": profile_serializer.data['image']['cover_image']

                        }

                        list.append(data)

                        return Response(list, status=status.HTTP_200_OK)
                    except ObjectDoesNotExist:
                            try:
                                profile_image = ProfileImage.objects.filter(user=i.to_user).get()

                                serializer = ProfileImageSerializer(profile_image)

                                if serializer:
                                    data = {
                                        "pk": i.to_user.id,
                                        "follower": i.to_user.follower_users_count,
                                        "nickname": i.to_user.nickname,
                                        "intro": '-',
                                        "profile_img": serializer.data['profile_image'],
                                        "cover_img": serializer.data['cover_image']

                                    }
                                    list.append(data)
                                    return Response(list, status=status.HTTP_200_OK)
                                raise exceptions.ValidationError('Abnormal connected')
                            except ObjectDoesNotExist:

                                    data = {
                                        "pk": i.to_user.id,
                                        "follower": i.to_user.follower_users_count,
                                        "nickname": i.to_user.nickname,
                                        "intro": '-',
                                        "profile_img": '/static/images/example/2.jpeg',
                                        "cover_img": '/static/images/example/1.jpeg'

                                    }
                                    list.append(data)
                                    return Response(list, status=status.HTTP_200_OK)

            else:
                return Response({}, status=status.HTTP_200_OK)

        else:
            follower = Relation.objects.filter(from_user=user)[0:4].get()

            list = []

            for i in follower:
                try:
                    profile = Profile.objects.filter(user=i.to_user).get()
                    profile_serializer = ProfileSerializer(profile)

                    data = {
                            "follower": i.to_user.follower_users_count,
                            "nickname": i.to_user.nickname,
                            "intro": profile_serializer.data['intro'],
                            "profile_img": profile_serializer.data['image']['profile_image'],
                            "cover_img": profile_serializer.data['image']['cover_image']


                    }
                    list.append(data)

                    return Response(list, status=status.HTTP_200_OK)
                except ObjectDoesNotExist:
                    raise exceptions.ValidationError({"detail": "must Register Profile"})

            return Response({},200)



