from django.db import models


class Notification(models.Model):
    # to_user = models.ForeignKey()
    # contents = models.ForeignKey()
    # from_user = models.ForeignKey()
    pass


class NotificationType(models.Model):
    NOTI_TYPE_POINT_CHARGE = 'pc'
    NOTI_TYPE_REWARD = 'r'
    NOTI_TYPE_WEB = 'w'
    CHOICES_USER_TYPE = (
        (NOTI_TYPE_POINT_CHARGE, 'Point-charge'),
        (NOTI_TYPE_REWARD, 'Reward'),
        (NOTI_TYPE_WEB, 'WebSite-use'),

    )
    user_type = models.CharField(
        max_length=1,
        choices=CHOICES_USER_TYPE,
    )

    pass