from django.db import models

# Create your models here.


class UsePoint(models.Model):
    type = models.CharField(max_length=255)
    point = models.PositiveIntegerField()

    class Meta:
        verbose_name = '사용 포인트'
        verbose_name_plural = f'{verbose_name} 목록'


class Product(models.Model):

    PRODUCT_TYPE_TESTER = '2200'
    PRODUCT_TYPE_STARTER = '5500'
    PRODUCT_TYPE_REGULAR = '11000'

    CHOICE_PRODUCT_TYPE = (
        (PRODUCT_TYPE_TESTER, 'Tester'),
        (PRODUCT_TYPE_STARTER, 'Starter'),
        (PRODUCT_TYPE_REGULAR, 'Regular'),
    )

    payment_type = models.CharField(
        max_length=255,
        choices=CHOICE_PRODUCT_TYPE,
        blank=False,
        default=None,
    )

