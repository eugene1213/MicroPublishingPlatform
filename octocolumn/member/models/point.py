from django.db import models

__all__ = (
    'PointHistory',
)


class PointHistory(models.Model):
    POINT_TYPE_CHARGE = 'c'
    POINT_TYPE_BUY = 'b'
    POINT_TYPE_REWARD = 'r'
    CHOICE_POINT_TYPE = (
        (POINT_TYPE_CHARGE,'Charge'),
        (POINT_TYPE_BUY, 'Buy'),
        (POINT_TYPE_REWARD, 'Reward'),

    )
    user = models.ForeignKey(
        'member.User',
        on_delete=models.CASCADE,
        null=True
                             )
    point_use_type = models.CharField(
        max_length=1,
        choices=CHOICE_POINT_TYPE,
        null=False,
        blank=False
    )

    point = models.IntegerField(default=0)
    history = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)