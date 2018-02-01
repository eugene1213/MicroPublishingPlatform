from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from django.db import models
from rest_framework.authtoken.models import Token


__all__ = (
    'UserManager',
    'User',
    'PointHistory',
    'BuyList'
)


class UserManager(DjangoUserManager):
    def create_superuser(self, username,email,password=None,*args,**kwargs):
        return super().create_superuser(username=username,email=email,password=password)

    def create_facebook_user(self, user_info):
        return self.create_user(
            username=user_info['id'],
            first_name=user_info.get('first_name', ''),
            last_name=user_info.get('last_name', ''),
            user_type=User.USER_TYPE_FACEBOOK
        )


class User(AbstractUser):
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_DJANGO = 'd'
    USER_TYPE_GOOGLE = 'g'
    USER_TYPE_TWITTER = 't'
    CHOICES_USER_TYPE = (
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_GOOGLE, 'Google'),
        (USER_TYPE_TWITTER, 'Twitter')
    )
    user_type = models.CharField(
        max_length=1,
        choices=CHOICES_USER_TYPE,
        default=USER_TYPE_DJANGO
    )
    created_at = models.DateField(auto_now_add=True)
    point=models.IntegerField(default=0)
    point_history = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='PointHistory',
        related_name='point_use_history',
    )


    # like_posts = models.ManyToManyField(
    #     'column.Post',
    #     related_name='like_users',
    #     blank=True,
    #     verbose_name='좋아요 누른 포스트 목록'
    # )
    # 내가 팔로우하고 있는 유저 목록
    #
    # 내가 A를 follow 한다
    #   나는 A의 follower이며
    #   A는 나의 followed_user이다

    # 나를 follow하고 있는 사람 목록은
    #   followers
    # 내가 follow하고 있는 사람 목록은
    #   followed_users
    following_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Relation',
        related_name='followers',
    )
    buy_list = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='BuyList',
        related_name='user_buylist',
    )
    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    @property
    def token(self):
        return Token.objects.get_or_create(user=self)[0].key

    def follow_toggle(self, user):
        # 1. 주어진 user가 User객체인지 확인
        #    아니면 raise ValueError()
        # 2. 주어진 user를 follow하고 있으면 해제
        #    안 하고 있으면 follow함
        if not isinstance(user, User):
            raise ValueError('"user" argument must be User instance!')

        relation, relation_created = self.following_user_relations.get_or_create(to_user=user)
        if relation_created:
            return True
        relation.delete()
        return False

        # if user in self.following_users.all():
        #     Relation.objects.filter(
        #         from_user=self,
        #         to_user=user,
        #     ).delete()
        # else:
        #     # Relation중개모델을 직접 사용하는 방법
        #     Relation.objects.create(
        #         from_user=self,
        #         to_user=user,
        #     )
        #     # Relation에 대한역참조 매니저를 사용하는 방법
        #     self.following_user_relations.create(to_user=user)


class Relation(models.Model):
    # User의 follow목록을 가질 수 있도록
    # MTM에 대한 중개모델을 구성
    # from_user, to_user, created_at으로 3개의 필드를 사용
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_user_relations',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower_relations',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Relation (' \
               f'from: {self.from_user.username}, ' \
               f'to: {self.to_user.username})'


class RelationProxy(Relation):
    class meta:
        proxy = True


class PointHistory(models.Model):
    POINT_TYPE_CHARGE = 'c'
    POINT_TYPE_BUY = 'b'
    POINT_TYPE_REWARD = 'r'
    CHOICE_POINT_TYPE = (
        (POINT_TYPE_CHARGE,'Charge'),
        (POINT_TYPE_BUY, 'Buy'),
        (POINT_TYPE_REWARD, 'Reward'),

    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_point_use_history',
        null=True
                             )
    point_use_type = models.CharField(
        max_length=1,
        choices=CHOICE_POINT_TYPE,
        null=False,
        blank=False
    )
    point = models.IntegerField(default=0)
    history = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class BuyList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buylist_user_relation',
        null=True
    )
    # post = models.ForeignKey(
    #     'column.Post',
    #     on_delete=models.CASCADE,
    #     related_name='buylist_post_relation',
    #     null=True
    #                          )
    post = models.CharField(blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)