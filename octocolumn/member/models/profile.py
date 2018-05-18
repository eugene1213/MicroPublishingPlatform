from django.db import models

# 저장 경로 파일 이름 설정


from utils.filepath import profile_cover_image_user_directory_path, profile_image_user_directory_path

__all__ =(
    'Profile',
    'ProfileImage'
)


class Profile(models.Model):

    user = models.ForeignKey('member.User', null=True, blank=True)
    # year = models.IntegerField(null=True,blank=True)
    #     # month = models.IntegerField(null=True, blank=True)
    #     # day = models.IntegerField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    intro = models.TextField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    web = models.CharField(max_length=255, null=True, blank=True)
    jobs = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255,null=True, blank=True)
    facebook = models.CharField(max_length=255,null=True, blank=True)
    instagram = models.CharField(max_length=255,null=True, blank=True)
    twitter = models.CharField(max_length=255,null=True, blank=True)
    subjects = models.CharField(max_length=255, null=True, blank=True)


class ProfileImage(models.Model):
    user = models.ForeignKey('member.User', null=True)
    cover_image = models.ImageField('포스트커버 이미지',
                                    upload_to=profile_cover_image_user_directory_path,
                                    blank=True,
                                    null=True,
                                    default='example/1.jpeg'
                                    )
    profile_image = models.ImageField('포스트프리뷰 이미지',
                                      upload_to=profile_image_user_directory_path,
                                      blank=True,
                                      null=True,
                                      default='example/2_x20_.jpeg'
                                      )
