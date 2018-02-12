import os
from django.db import models

# 저장 경로 파일 이름 설정
from django.utils import timezone


__all__ =(
    'Profile',
    'ProfileImage'
)


def set_filename_format(now, instance, filename):
    """ file format setting e.g) {username}-{date}-{microsecond}{extension} hjh-2016-07-12-158859.png """
    return "{username}-{date}-{microsecond}{extension}".format(
        username=instance.user.username,
        date=str(now.date()),
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[1], )


#저장 경로 디렉토리 설정
def user_directory_path(instance, filename):
    """ image upload directory setting e.g)
     images/{year}/{month}/{day}/{username}/{filename}
     images/2016/7/12/hjh/hjh-2016-07-12-158859.png """
    now = timezone.now()
    path = "profile-images/{username}/{year}/{month}/{day}/{filename}".format(
        year=now.year,
        username=instance.user.username,
        month=now.month,
        day=now.day,
        filename=set_filename_format(now, instance,
                                     filename), )
    return path


class Profile(models.Model):
    SEX_TYPE_MALE = 'm'
    SEX_TYPE_FEMALE = 'f'
    CHOICES_USER_TYPE = (
        (SEX_TYPE_MALE, 'm'),
        (SEX_TYPE_FEMALE, 'f'),
    )
    user = models.ForeignKey('User', null=True)
    birth = models.DateField(null=True)
    sex = models.CharField(
        max_length=1,
        choices=CHOICES_USER_TYPE,
        null=True
    )
    phone = models.CharField(max_length=100,null=True)
    jobs = models.CharField(max_length=255, null=True)
    interview = models.CharField(max_length=255, null=True)
    region = models.CharField(max_length=255,null=True)


class ProfileImage(models.Model):
    file = models.FileField('프로필 이미지',
                            upload_to=user_directory_path,
                            blank=True)