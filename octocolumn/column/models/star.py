from django.db import models

__all__ = (
    'PostStar',
)


class PostStar(models.Model):

    content = models.IntegerField(
        default=0,
    )

    member_num = models.IntegerField(default=0)
    updated_date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey('column.Post', null=True)

