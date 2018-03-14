from django.db import models

from utils.filepath import temp_user_directory_path

__all__ = (
    'Temp',
    'TempFile'
)


class Temp(models.Model):
    author = models.ForeignKey('member.User', null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    main_content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {} : {} : {}'.format(
            self.author,
            self.title,
            self.main_content,
            self.created_date
        )


class TempFile(models.Model):
    author = models.ForeignKey('member.User',null=True)
    file = models.FileField('포스트파일저장 이미지',
                            upload_to=temp_user_directory_path,
                            blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


