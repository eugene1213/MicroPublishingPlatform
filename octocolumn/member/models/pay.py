from django.db import models

from member.models import PointHistory

__all__ = (
    # 'OrderNumber',
    'PayListManager',
    'PayList'
)


class PayListManager(models.Manager):

    def preview(self, user, price=None, content=None, order_number=None):
        instance = self.model(
            user=user,
            payment_type=PayList.PAYMENT_TYPE_CARD,
            price=price,
            content=content,
            order_number=order_number

        )
        # user.point += int(price)
        # PointHistory.objects.charge(user=user, point=int(price), history='카드')
        # user.save()
        instance.save()
        return instance

    def card(self, user, price, content, order_number=None):
        instance = self.model(
            user=user,
            payment_type=PayList.PAYMENT_TYPE_CARD,
            price=price,
            content=content,
            order_number=order_number
        )
        user.point += int(price) - int(price/1.1)
        PointHistory.objects.charge(user=user, point=int(price), history='카드')
        user.save()
        instance.save()
        return instance

    def bank(self, user, price, content, order_number=None):
        instance = self.model(
            user=user,
            payment_type=PayList.PAYMENT_TYPE_BANK,
            price=price,
            content=content,
            order_number=order_number

        )
        user.point += int(price) - int(price/1.1)
        PointHistory.objects.charge(user=user, point=int(price), history='은행')
        user.save()
        instance.save()
        return instance

    def phone(self, user, price, content, order_number=None):
        instance = self.model(
            user=user,
            payment_type=PayList.PAYMENT_TYPE_PHONE,
            price=price,
            content=content,
            order_number=order_number
        )
        user.point += int(price) - int(price/1.1)
        PointHistory.objects.charge(user=user, point=int(price), history='소액결제')
        user.save()
        instance.save()
        return instance

    def cancel(self, user, price, content):
        instance = self.model(
            user=user,
            payment_type=PayList.PAYMENT_TYPE_CANCEL,
            price=price,
            content=content
        )
        user.point -= int(price) - int(price/1.1)
        user.save()
        instance.save()
        return instance


class PayList(models.Model):
    PAYMENT_TYPE_CARD = '카드'
    PAYMENT_TYPE_BANK = '은행'
    PAYMENT_TYPE_PHONE = '소액결제'
    PAYMENT_TYPE_CANCEL = '취소'

    STATUS_TYPE_CONFIRM = '승인'
    STATUS_TYPE_HOLD = '보류'
    STATUS_TYPE_CANCEL = '취소'

    CHOICE_PAYMENT_TYPE = (
        (PAYMENT_TYPE_CARD, 'Card'),
        (PAYMENT_TYPE_BANK, 'Bank'),
        (PAYMENT_TYPE_PHONE, 'Phone'),
        (PAYMENT_TYPE_CANCEL, 'Cancel'),
    )

    CHOICE_STATUS_TYPE = (
        (STATUS_TYPE_CONFIRM, '승인'),
        (STATUS_TYPE_HOLD, '보류'),
        (STATUS_TYPE_CANCEL, '취소'),
    )

    user = models.ForeignKey('member.User')
    content = models.CharField(max_length=255)
    payment_type = models.CharField(
        max_length=255,
        choices=CHOICE_PAYMENT_TYPE,
        blank=True,
        default=None,
        null=True
    )
    price = models.IntegerField(null=True)
    check = models.BooleanField(default=False)
    status = models.CharField(
        max_length=255,
        choices=CHOICE_STATUS_TYPE,
        blank=True,
        default=None,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    order_num = models.CharField(null=True, max_length=255, unique=True)

    objects = PayListManager()

    class Meta:
        verbose_name = '결제 내역'
        verbose_name_plural = f'{verbose_name} 목록'


# class OrderNumber(models.Model):
#     order_number = models.CharField(unique=True)
#
#     def save(self, *args, **kwargs):
#         OrderNumber.objects.filter(order_number_gte=self.order_number).update(
#             order_number=F("accvalue")+1)
#         super(OrderNumber, self).save(*args, **kwargs)


# order_number = str(DateFormat(datetime.now()).format('Ymd')))
