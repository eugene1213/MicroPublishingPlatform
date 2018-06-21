from django.db import models

__all__ = (
    'Notification',
)


class Notification(models.Model):
    post = models.ForeignKey(
        'column.Post',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    comment = models.ForeignKey(
        'column.Comment',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    contents = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



