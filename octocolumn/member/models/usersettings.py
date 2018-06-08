from django.db import models

__all__ = (
    'UserSettings',
)


class UserSettings(models.Model):
    user = models.OneToOneField('member.User')
    phone = models.BooleanField(default=False)
    birthday = models.BooleanField(default=False)
    sex = models.BooleanField(default=False)
    jobs = models.BooleanField(default=False)
    web = models.BooleanField(default=False)
    facebook = models.BooleanField(default=False)
    instagram = models.BooleanField(default=False)
    email = models.BooleanField(default=False)
    subjects = models.BooleanField(default=False)
    twitter = models.BooleanField(default=False)
#




