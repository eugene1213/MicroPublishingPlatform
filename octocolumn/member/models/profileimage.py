import os
from django.db import models

# 저장 경로 파일 이름 설정
from django.utils import timezone


__all__ =(
    'ProfileImage',
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
    path = "profileimages/{username}/{year}/{month}/{day}/{filename}".format(
        year=now.year,
        username=instance.user.username,
        month=now.month,
        day=now.day,
        filename=set_filename_format(now, instance,
                                     filename), )
    return path


class ProfileImage(models.Model):
    user = models.ForeignKey('member.User',null=True)
    file = models.FileField('프로필 이미지',
                            upload_to=user_directory_path,
                            blank=True)