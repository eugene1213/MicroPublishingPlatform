from django.db import models


__all__ = (
    'Author',
)


class Author(models.Model):
    author = models.OneToOneField('member.User', unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    intro = models.CharField(max_length=255, null=True)
    blog = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = '작가'
        verbose_name_plural = f'{verbose_name} 목록'
