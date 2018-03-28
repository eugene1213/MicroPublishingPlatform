from django.db import models


class InvitationUser(models.Model):
    email = models.EmailField(max_length=255)