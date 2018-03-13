from django.db import models


__all__ = (
    'ConnectedLog',
)


class ConnectedLog(models.Model):
    TYPE_LOGIN = 'login'
    TYPE_LOGOUT = 'logout'
    LOG_TYPE = (
        (TYPE_LOGIN, 'Log-in'),
        (TYPE_LOGOUT, 'Log-out'),

    )
    user = models.ForeignKey('User')
    ip_address = models.GenericIPAddressField(verbose_name= ('IP Address',))
    user_agent = models.CharField(
        verbose_name=('HTTP User Agent',),
        max_length=300,
    )
    type = models.CharField(
        max_length=50,
        choices=LOG_TYPE,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ('접속 기록',)
        ordering = ('-created_at',)

