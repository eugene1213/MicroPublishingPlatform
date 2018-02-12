from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import (
    PermissionsMixin)
from django.db import models
from django.db.models import F
from rest_framework.authtoken.models import Token


__all__ = (
    'UserManager',
    'User',
)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, user_type, password=None):
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, last_name, first_name, password=None, *args,**kwargs):
        user = self.model(
            email=email,
            last_name=last_name,
            first_name=first_name,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def create_facebook_user(self, user_info):
        return self.create_user(
            email=user_info['id'],
            first_name=user_info.get('first_name', ''),
            last_name=user_info.get('last_name', ''),
            user_type=User.USER_TYPE_FACEBOOK
        )

    def create_google_user(self, user_info):
        return self.create_user(
            email=user_info['id'],
            first_name=user_info.get('first_name', ''),
            last_name=user_info.get('last_name', ''),
            user_type=User.USER_TYPE_FACEBOOK
        )

    def create_twitter_user(self, user_info):
        return self.create_user(
            email=user_info['id'],
            first_name=user_info.get('first_name', ''),
            last_name=user_info.get('last_name', ''),
            user_type=User.USER_TYPE_FACEBOOK
        )


class User(AbstractBaseUser, PermissionsMixin):
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
    email = models.EmailField(unique=True)
    created_at = models.DateField(auto_now_add=True)
    point = models.IntegerField(default=0)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

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
    user_buylist = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='BuyList',
        related_name='buy_list',
    )
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'last_name',
        'first_name'
    ]

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

    # 포인트 증가
    def increase_point(self, point):
        self.point = F('point') + point
        self.save()

    # 포인트 감소
    def decrease_point(self, point):
        self.point = F('point') - point
        self.save()


class Relation(models.Model):
    # User의 follow목록을 가질 수 있도록
    # MTM에 대한 중개모델을 구성
    # from_user, to_user, created_at으로 3개의 필드를 사용
    from_user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='following_user_relations',
    )
    to_user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='follower_relations',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Relation (' \
               f'from: {self.from_user.email}, ' \
               f'to: {self.to_user.email})'


class RelationProxy(Relation):
    class meta:
        proxy = True


class BuyList(models.Model):
    # User의 follow목록을 가질 수 있도록
    # MTM에 대한 중개모델을 구성
    # user, buy_list, created_at으로 3개의 필드를 사용
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='buylist_user_relation',
        null=True
    )
    post_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'BuyList (' \
               f'from: {self.user.email}, ' \
               f'to: {self.post.title})'






