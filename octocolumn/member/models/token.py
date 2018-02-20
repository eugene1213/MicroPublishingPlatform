from django.db import models


class EmailToken(models.Model):
    VERIFY_TYPE_CHANGE_PASSWORD = 'cp'
    VERIFY_TYPE_SIGNUP = 'su'
    CHOICES_TOKEN_TYPE = (
        (VERIFY_TYPE_SIGNUP, 'SignUp'),
        (VERIFY_TYPE_CHANGE_PASSWORD, 'Change_password'),
    )
    user = models.OneToOneField('member.User', null=True)
    verify_type = models.CharField(
        max_length=50,
        choices=CHOICES_TOKEN_TYPE,
    )
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
