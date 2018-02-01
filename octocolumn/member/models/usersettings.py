from django.db import models


__all__ = (
    'UserSecondPassword',
    'UserSetting'
)


class UserSecondPassword(models.Model):
    user = models.ForeignKey('member.User',null=True)
    second_password = models.IntegerField(default=None)

    def __str__(self):
        return '{} : {}'.format(
            self.user,
            self.second_password,
        )


class UserSetting(models.Model):
    user = models.ForeignKey('member.User',null=True)

    def __str__(self):
        return '{} : {}'.format(
            self.user,
        )

