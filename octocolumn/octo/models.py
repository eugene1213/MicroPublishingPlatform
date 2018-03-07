from django.db import models

# Create your models here.


class UsePoint(models.Model):
    type = models.CharField(max_length=255)
    point = models.PositiveIntegerField()


