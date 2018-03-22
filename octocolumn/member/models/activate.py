from django.db import models


__all__ = (
    'InviteUser',
)


class InviteUser(models.Model):
    email = models.CharField(max_length=255)