from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from django.contrib import admin
from django.utils.safestring import mark_safe

from octo.models import UsePoint
from column.models import Post

import re

from member.models import User, Author, PointHistory
from utils.filters import CreatedDateFilter, UsePointFilter

admin.site.unregister(Group)
admin.site.unregister(Token)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['username', 'first_name', 'nickname', 'last_name', 'point', 'user_type', 'created_at', 'post_count',
                    'is_active']
    list_display_links = ['username']
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('-id', 'username')
    fieldsets = (
        ['기본 정보', {
            'fields': ('username', 'nickname', 'last_name', 'first_name',),
        }],
        ['접속 정보', {
            'fields': ('last_login',),
        }],
        ['정보', {
            'fields': ('created_at', 'point', 'post_count', 'is_active')
        }]

    )

    readonly_fields = ['username', 'last_name', 'first_name', 'post_count', 'created_at', 'is_active', 'last_login']

    def post_count(self, obj):
        return Post.objects.filter(author=obj).count()

    def has_add_permission(self, request):
        return False

    post_count.short_description = '포스팅'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['author', 'is_active', 'intro', 'blog', 'created_at']
    list_display_links = ['author']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id', 'title', 'created_date', 'author', 'content_size', 'hit', 'buy_count']
    list_display_links = ['id', 'title']
    search_fields = ('author__username',)
    ordering = ('-id', '-created_date')
    list_filter = (CreatedDateFilter,)

    fieldsets = (
        ['기본 정보', {
            'fields': ('author',),
        }],
        ['컬럼 정보', {
            'fields': ('title', 'main_content',),
        }],
        ['구매 정보', {
            'fields': ('hit', 'price', 'created_date', 'buy_count')
        }]

    )

    readonly_fields = ['author', 'hit', 'buy_count', 'created_date']

    class Meta:
        verbose_name = '작가'
        verbose_name_plural = f'{verbose_name} 목록'

    def remove_tag(self, post):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', post)
        return clean_text

    def content_size(self, post):
        clean_text = self.remove_tag(post.main_content)
        return mark_safe('<u>{}</u>글자'.format(len(clean_text)))

    content_size.short_description = '글자수'


@admin.register(UsePoint)
class PublishPointAdmin(admin.ModelAdmin):
    list_display = ['type', 'point']
    list_display_links = ['type', 'point']


@admin.register(PointHistory)
class PointHistoryAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['user', 'point', 'point_use_type', 'created_at']
    search_fields = ('user__username',)
    actions = None
    list_filter = (UsePointFilter,)

    class Meta:
        label = '포인트 사용내역'

    def has_add_permission(self, request):
        return False






