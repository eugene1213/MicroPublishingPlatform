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
            to_user = User.objects.filter(pk=user_pk).get()
            result, relation = Relation.objects.get_or_create(to_user=to_user, from_user= self.request.user)

            if result:
                return Response({'detail': 'created',
                                 "author":{
                                     "follow_status": True,
                                     "follower": Relation.objects.filter(from_user=from_user).count()
                                 }
                                 })

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
                return Response({'detail': 'created'})
            return Response({'created': 'deleted'})

        except ObjectDoesNotExist:
            raise exceptions.ValidationError({"detail": "Abnormal connected"})


class GetUserFollowingCard(ListAPIView):
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
                                "follower": Relation.objects.filter(to_user=i.to_user).count(),
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
                                        "follower": Relation.objects.filter(to_user=i.to_user).count(),
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
                                        "follower": Relation.objects.filter(to_user=i.to_user).count(),
                                        "nickname": i.to_user.nickname,
                                        "intro": '-',
                                        "profile_img": '/static/images/example/2_x20_.jpeg',
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
                            "follower": Relation.objects.filter(to_user=i.to_user).count(),
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

    def follower_status(self, user):
        try:
            Relation.objects.filter(to_user=self.request.user, from_user=user).get()
            return True
        except ObjectDoesNotExist:
            return False

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

                        profile = Profile.objects.filter(user=i.from_user).get()
                        profile_serializer = ProfileSerializer(profile)

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

                        return Response(list, status=status.HTTP_200_OK)
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
                                    return Response(list, status=status.HTTP_200_OK)
                                raise exceptions.ValidationError('Abnormal connected')
                            except ObjectDoesNotExist:

                                    data = {
                                        "pk": i.from_user.id,
                                        "follower": Relation.objects.filter(from_user=i.from_user).count(),
                                        "nickname": i.from_user.nickname,
                                        "follow_status": self.follower_status(i.from_user),
                                        "intro": '-',
                                        "profile_img": '/static/images/example/2_x20_.jpeg',
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
                    profile = Profile.objects.filter(user=i.from_user).get()
                    profile_serializer = ProfileSerializer(profile)

                    data = {
                            "follower": Relation.objects.filter(from_user=i.from_user).count(),
                            "nickname": i.from_user.nickname,
                            "intro": profile_serializer.data['intro'],
                            "follow_status": self.follower_status(i.from_user),
                            "profile_img": profile_serializer.data['image']['profile_image'],
                            "cover_img": profile_serializer.data['image']['cover_image']


                    }
                    list.append(data)

                    return Response(list, status=status.HTTP_200_OK)
                except ObjectDoesNotExist:
                    raise exceptions.ValidationError({"detail": "must Register Profile"})

            return Response({},200)



