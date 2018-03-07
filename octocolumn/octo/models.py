from django.db import models

# Create your models here.


class PublishPoint(models.Model):
    type = models.ForeignKey('PointType', null=True)
    point = models.PositiveIntegerField()


class PointType(models.Model):
    type = models.CharField(max_length=255)