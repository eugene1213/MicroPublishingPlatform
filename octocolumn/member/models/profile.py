import os
from django.db import models

# 저장 경로 파일 이름 설정


from utils.filepath import profile_cover_image_user_directory_path, profile_image_user_directory_path

__all__ =(
    'Profile',
    'ProfileImage'
)


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
    phone = models.CharField(max_length=100, null=True)
    intro = models.TextField()
    jobs = models.CharField(max_length=255, null=True)
    interview = models.CharField(max_length=255, null=True)
    region = models.CharField(max_length=255,null=True)


class ProfileImage(models.Model):
    user = models.ForeignKey('member.User', null=True)
    cover_image = models.ImageField('포스트커버 이미지',
                                    upload_to=profile_cover_image_user_directory_path,
                                    blank=True,
                                    null=True
                                    )
    profile_image = models.ImageField('포스트프리뷰 이미지',
                                      upload_to=profile_image_user_directory_path,
                                      blank=True,
                                      null=True
                                      )