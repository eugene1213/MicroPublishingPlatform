# 저장 경로 파일 이름 설정
import os

from django.utils import timezone


def set_filename_format(now, instance, filename):
    """ file format setting e.g) {username}-{date}-{microsecond}{extension} hjh-2016-07-12-158859.png """
    return "{username}-{date}-{microsecond}{extension}".format(
        username=instance.author.pk,
        date=str(now.date()),
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[1],
    )


def user_set_filename_format(now, instance, size ,filename):
    """ file format setting e.g) {username}-{date}-{microsecond}{extension} hjh-2016-07-12-158859.png """
    return "{username}-{date}-{microsecond}-{size}-{extension}".format(
        username=instance.user.pk,
        date=str(now.date()),
        microsecond=now.microsecond,
        size=size,
        extension=os.path.splitext(filename)[1],
    )


#저장 경로 디렉토리 설정
def temp_user_directory_path(instance, filename):
    """ image upload directory setting e.g)
     images/{year}/{month}/{day}/{username}/{filename}
     images/2016/7/12/hjh/hjh-2016-07-12-158859.png """
    print()
    now = timezone.now()
    path = "post-image/{username}/{year}/{month}/{day}/{filename}".format(
        username=instance.author.pk,
        year=now.year,
        month=now.month,
        day=now.day,
        filename=set_filename_format(now, instance,
                                     filename), )
    return path


def cover_image_user_directory_path(instance, filename):
    """ image upload directory setting e.g)
     images/{year}/{month}/{day}/{username}/{filename}
     images/2016/7/12/hjh/hjh-2016-07-12-158859.png """
    now = timezone.now()
    path = "post-image/cover/{username}/{year}/{month}/{day}/{filename}".format(
        username=instance.author.pk,
        year=now.year,
        month=now.month,
        day=now.day,
        filename=set_filename_format(now, instance,
                                     filename), )
    return path


def preview_image_user_directory_path(instance, filename):
    """ image upload directory setting e.g)
     images/{year}/{month}/{day}/{username}/{filename}
     images/2016/7/12/hjh/hjh-2016-07-12-158859.png """
    now = timezone.now()
    path = "post-image/preview/{username}/{year}/{month}/{day}/{filename}".format(
        username=instance.author.pk,
        year=now.year,
        month=now.month,
        day=now.day,
        filename=set_filename_format(now, instance,
                                     filename), )
    return path


def profile_image_user_directory_path(instance, filename):
    """ image upload directory setting e.g)
     images/{year}/{month}/{day}/{username}/{filename}
     images/2016/7/12/hjh/hjh-2016-07-12-158859.png """
    now = timezone.now()
    path = "profile/profile/{username}/{year}/{month}/{day}/{filename}".format(
        username=instance.user.pk,
        year=now.year,
        month=now.month,
        day=now.day,
        filename=user_set_filename_format(now, instance,
                                     filename), )
    return path


def profile_cover_image_user_directory_path(instance, filename, size):
    """ image upload directory setting e.g)
     images/{year}/{month}/{day}/{username}/{filename}
     images/2016/7/12/2016-07-12-158859.png """
    now = timezone.now()
    path = "profile/cover/{username}/{year}/{month}/{day}/{filename}".format(
        username=instance.user.pk,
        year=now.year,
        month=now.month,
        day=now.day,
        filename=user_set_filename_format(now, instance,
                                     filename, size), )
    return path