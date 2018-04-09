from django.db import models
from django.db.models import F

__all__ = (
    'OctoCode',
    # 'UserSetting'
)


class OctoCode(models.Model):
    user = models.OneToOneField('member.User', null=True)
    octo_code = models.CharField(max_length=255)
    error_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} : {}'.format(
            self.user,
            self.octo_code,
            self.error_count
        )

    # 오입력시 카운트 증가 시키는 메서드
    def increase(self, user):
        user.error_count = F('error_count') + 1
        user.save()

    # 비밀번호 오입력시 카운트를 초기화 시키는 메서드
    def decrease(self, user):
        user.error_count = 0
        user.save()

#
# class UserSetting(models.Model):
#     user = models.ForeignKey('member.User', null=True)
#
#     def __str__(self):
#         return '{} : {}'.format(
#             self.user,
#             self.octo_code
#         )

