from django.db import models
from django.db.models import F

__all__ = (
    'OtherPassword',
    'UserSetting'
)


class OtherPassword(models.Model):
    user = models.ForeignKey('User', null=True)
    second_password = models.CharField(max_length=255)
    error_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} : {}'.format(
            self.user,
            self.second_password,
            self.e_count
        )

    # 오입력시 카운트 증가 시키는 메서드
    def increase(self):
        self.error_count = F('error_count') + 1
        self.save()

    # 비밀번호 오입력시 카운트를 초기화 시키는 메서드
    def decrease(self):
        self.error_count = 0
        self.save()


class UserSetting(models.Model):
    user = models.ForeignKey('User', null=True)

    def __str__(self):
        return '{} : {}'.format(
            self.user,
        )

