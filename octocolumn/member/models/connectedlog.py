from django.db import models


__all__ = (
    'ConnectedLog',
)


class ConnectedLog(models.Model):
    user = models.ForeignKey('User')
    ip_address = models.GenericIPAddressField(verbose_name= ('IP Address',))
    user_agent = models.CharField(
        verbose_name=('HTTP User Agent',),
        max_length=300,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ('접속 기록',)
        ordering = ('-created_at',)

