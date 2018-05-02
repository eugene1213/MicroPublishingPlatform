import datetime

from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import Coalesce

from column.models import Post
from member.models import PointHistory


class CreatedDateFilter(admin.SimpleListFilter):
    title = '작성일'
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        results = []
        for i in range(-3, 6):
            date = datetime.date.today() + datetime.timedelta(days=i)
            display_str = '{0} [{1}]'.format(
                date,
                Post.objects.filter(created_date__date=date).count()
            )
            display_str += ' - 오늘' if i==0 else ''
            results.append((date, display_str))

        return results

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(created_date__date=self.value())
        else:
            return queryset.all()


class UsePointFilter(admin.SimpleListFilter):
    title = '발행에 사용된 포인트'
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        results = []
        for i in range(-7, 1):
            date = datetime.date.today() + datetime.timedelta(days=i)
            display_str = '{0} [{1}]'.format(
                date,
                PointHistory.objects.filter(created_at__date=date, point_use_type='구매').aggregate(
                    total=Coalesce(Sum('point'), 0))['total']
            )
            display_str += ' - 오늘' if i==0 else ''
            results.append((date, display_str))

        return results

    def queryset(self, request, queryset):
        if self.value():
            if self.value() is None:
                return queryset.filter(created_at__date=self.value())
        else:
            return queryset.all()
