
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import (
    PermissionsMixin)
from django.db import models

from column.models import Post

__all__ = (
    'UserManager',
    'User',
    'BuyList',
    'SellList'
)


class UserManager(BaseUserManager):
    def create_user(self, username, nickname, password=None):
        user = self.model(
            username=username,
            nickname=nickname
        )
        user.user_type = 'd'
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, *args,**kwargs):
        user = self.model(
            username=username,
            nickname='Superuser',

        )
        user.is_active = True
        user.user_type = 'd'
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    #
    def create_facebook_user(self, username, nickname, social_id):
        user = self.model(
            username=username,
            nickname=nickname,
            social_id=social_id,
        )
        user.user_type = 'f'
        user.set_unusable_password()
        user.is_active = True
        user.save()
        return user

    def create_google_user(self, username,nickname,social_id):
        user = self.model(
            username=username,
            nickname=nickname,
            social_id=social_id,
        )
        user.user_type = 'g'
        user.set_unusable_password()
        user.is_active = True
        user.save()
        return user

    def create_kakao_user(self, username,nickname,social_id):
        user = self.model(
            username=username,
            nickname=nickname,
            social_id=social_id
        )
        user.user_type = 'k'
        user.set_unusable_password()
        user.is_active = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_FACEBOOK = 'fb'
    USER_TYPE_DJANGO = 'd'
    USER_TYPE_GOOGLE = 'g'
    USER_TYPE_KAKAO = 'k'
    CHOICES_USER_TYPE = (
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_GOOGLE, 'Google'),
        (USER_TYPE_KAKAO, 'Kakao')
    )
    user_type = models.CharField(
        max_length=50,
        choices=CHOICES_USER_TYPE,
        default='d'
    )
    username = models.EmailField(unique=True)
    social_id = models.CharField(null=True, max_length=255)
    point = models.IntegerField(default=500)
    nickname = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

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
    waiting_user = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='WaitingRelation',
        related_name='waiting',

    )
    bookmark = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Bookmark',
        related_name='bookmark_relation',
    )

    buy_list = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='BuyList',
        related_name='buylist_relation',
    ),

    sell_list = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='SellList',
        related_name='selllist_relation',
    ),

    point_history = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='PointHistory',
        related_name='pointhistory_relation_set',
    ),

    # notification = models.ManyToManyField(
    #     'member.notification',
    #     related_name='recommand',
    #     blank=True,
    #     null=True
    # )

    objects = UserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = [
        'last_name',
        'first_name'
    ]

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    def get_full_name(self):
        return self.last_name + self.first_name

    def get_short_name(self):
        return self.first_name

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


# 팔로우 다대다
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
               f'from: {self.from_user.username}, ' \
               f'to: {self.to_user.username})'


class RelationProxy(Relation):
    class meta:
        proxy = True


# 기다림
class WaitingRelation(models.Model):
    # User의 follow목록을 가질 수 있도록
    # MTM에 대한 중개모델을 구성
    # from_user, to_user, created_at으로 3개의 필드를 사용
    receive_user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='waiting_from_user_relations',
    )
    send_user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='waiting_send_relations',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Relation (' \
               f'from: {self.receive_user.username}, ' \
               f'to: {self.send_user.username})'


class BuyList(models.Model):
    # User의 buy_list 가질 수 있도록
    # MTM에 대한 중개모델을 구성
    # user, post, created_at으로 3개의 필드를 사용
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='buylist_user_relation',
        null=True
    )
    post = models.ForeignKey('column.Post', null=True)
    order_number = models.CharField(max_length=200, null=True, blank=True)
    star = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'BuyList (' \
               f'from: {self.user.username}, ' \
               f'to: {self.post.title})'


class SellList(models.Model):
    # User의 sell_list 가질 수 있도록
    # MTM에 대한 중개모델을 구성
    # user, post, created_at으로 3개의 필드를 사용
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='sell_list_user_relation',
        null=True
    )
    post = models.ForeignKey('column.Post', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'SellList (' \
               f'from: {self.user.username}, ' \
               f'to: {self.post.title})'


class Bookmark(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='bookmark_user_relation',
        null=True
    )
    post = models.ForeignKey(
        'column.Post',
        on_delete=models.CASCADE,
        related_name='bookmark_post_relations',
        null=True)
    created_at = models.DateTimeField(auto_now_add=True)



