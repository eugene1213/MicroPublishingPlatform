from django.db import models

__all__ = (
    'BuyList',
)


class BuyList(models.Model):
    user = models.ForeignKey(
        'member.User',
        on_delete=models.CASCADE,
        related_name='buylist_user_relation',
        null=True
    )
    post = models.ForeignKey(
        'column.Post',
        on_delete=models.CASCADE,
        related_name='buylist_post_relation',
        null=True
                             )
    created_at = models.DateTimeField(auto_now_add=True)