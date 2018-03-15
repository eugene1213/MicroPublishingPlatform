from django.db import models

# 저장 경로 파일 이름 설정


from utils.filepath import profile_cover_image_user_directory_path, profile_image_user_directory_path

__all__ =(
    'Profile',
    'ProfileImage'
)


class Profile(models.Model):

    user = models.ForeignKey('member.User', null=True)
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    day = models.IntegerField
    sex = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=100, null=True)
    intro = models.TextField(null=True)
    age = models.IntegerField(null=True)
    jobs = models.CharField(max_length=255, null=True)
    region = models.CharField(max_length=255,null=True)
    facebook = models.CharField(max_length=255,null=True)
    instagram = models.CharField(max_length=255,null=True)
    twitter = models.CharField(max_length=255,null=True)
    subjects = models.CharField(max_length=255, null=True)


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
