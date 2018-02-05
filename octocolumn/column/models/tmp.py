import os
from django.db import models
from django.utils import timezone

__all__ = (
    'Temp',
    'TempFile'
)


# 저장 경로 파일 이름 설정
def set_filename_format(now, instance, filename):
    """ file format setting e.g) {username}-{date}-{microsecond}{extension} hjh-2016-07-12-158859.png """
    return "{username}-{date}-{microsecond}{extension}".format(
        username=instance.author.pk,
        date=str(now.date()),
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[1],
    )


#저장 경로 디렉토리 설정
def user_directory_path(instance, filename):
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


class Temp(models.Model):
    author = models.ForeignKey('member.User', null=True)
    title = models.CharField(max_length=255,blank=True,null=True)
    main_content = models.TextField()
    modified_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {} : {} : {}'.format(
            self.author,
            self.title,
            self.main_content,
            self.modified_date
        )


class TempFile(models.Model):
    author = models.ForeignKey('member.User',null=True)
    file = models.FileField('포스트파일저장 이미지',
                            upload_to=user_directory_path,
                            blank=True)
    created_at = models.DateTimeField(auto_now_add=True)