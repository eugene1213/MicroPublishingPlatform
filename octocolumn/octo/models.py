from django.db import models

# Create your models here.


class UsePoint(models.Model):
    type = models.CharField(max_length=255)
    point = models.PositiveIntegerField()

    class Meta:
        verbose_name = '사용 포인트'
        verbose_name_plural = f'{verbose_name} 목록'


