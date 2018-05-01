
from django.conf.urls import url
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse

from django.urls import reverse
from django.utils.html import format_html
from rest_framework.authtoken.models import Token
from django.contrib import admin
from django.utils.safestring import mark_safe

from member.forms import AuthorIsActive, PostDraftAction
from octo.models import UsePoint
from column.models import Post, PreAuthorPost

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

    # fieldsets = (
    #     ['기본 정보', {
    #         'fields': ('author',),
    #     }],
    #     ['컬럼 정보', {
    #         'fields': ('title', 'main_content',),
    #     }],
    #     ['구매 정보', {
    #         'fields': ('hit', 'price', 'created_date', 'buy_count')
    #     }]
    #
    # )

    fields = (
        'author', 'hit', 'price', 'cover_image', 'created_date', 'post_download',
    )

    readonly_fields = ['author', 'hit', 'buy_count', 'created_date', 'post_download']

    class Meta:
        verbose_name = '작가'
        verbose_name_plural = f'{verbose_name} 목록'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<post_pk>.+)/download/$',
                self.admin_site.admin_view(self.process_download),
                name='postDownload',
            )
        ]
        return custom_urls + urls

    def post_download(self, obj):
        return format_html(
         '<a class="button" href="{}">다운로드</a>',
            reverse('admin:postDownload', args=[obj.pk]),
        )

    def process_download(self, request, post_pk, *args, **kwargs):
        return self.download_action(
            request=request,
            post_pk=post_pk,
        )

    def download_action(self, request, post_pk):
        main_con = Post.objects.filter(pk=post_pk).get().main_content
        contents = '<div class="main_content_wrap">' + main_con + '</div>'
        read_css = \
            '<link rel="stylesheet" type="text/css" href="https://static.octocolumn.com/static/css/sass/read.css">'
        sub_css = \
            '<link rel="stylesheet" type="text/css" href="https://static.octocolumn.com/static/css/sass/sub.css">'
        response = HttpResponse(read_css + sub_css + contents)
        return response

    def remove_tag(self, obj):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', obj)
        return clean_text

    def content_size(self, post):
        clean_text = self.remove_tag(post.main_content)
        return mark_safe('<u>{}</u>글자'.format(len(clean_text)))

    content_size.short_description = '글자수'
    post_download.allow_tags = True


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


@admin.register(PreAuthorPost)
class PreAuthorPostAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = [
        'author', 'title', 'content_size', 'price', 'author_is_active', 'created_date', 'author_actions',
                    'author_draft',
                    ]

    # fieldsets = (
    #     ['기본 정보', {
    #         'fields': ('author',),
    #     }],
    #     ['컬럼 정보', {
    #         'fields': ('title', 'main_content',),
    #     }],
    #     ['구매 정보', {
    #         'fields': ('price', 'created_date')
    #     }]
    #
    # )

    fields = (
        'author', 'price', 'cover_image','author_actions', 'post_download', 'created_date'
    )

    readonly_fields = ['author', 'author_actions', 'post_download', 'created_date']

    def author_is_active(self, instance):
        return instance.author.author.is_active

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<author_post_pk>.+)/active/$',
                self.admin_site.admin_view(self.process_is_active),
                name='authorIsActive',
            ),
            url(
                r'^(?P<author_post_pk>.+)/draft/$',
                self.admin_site.admin_view(self.process_is_draft),
                name='authorDraft',
            ),
            url(
                r'^(?P<post_pk>.+)/download/$',
                self.admin_site.admin_view(self.process_download),
                name='postDownload',
            )
        ]
        return custom_urls + urls

    def post_download(self, obj):
        return format_html(
         '<a class="button" href="{}">다운로드</a>',
            reverse('admin:postDownload', args=[obj.pk]),
        )

    def process_download(self, request, post_pk, *args, **kwargs):
        return self.download_action(
            request=request,
            post_pk=post_pk,
        )

    def download_action(self, request, post_pk):
        main_con = PreAuthorPost.objects.filter(pk=post_pk).get().main_content
        contents = '<div class="main_content_wrap">' + main_con + '</div>'
        read_css = \
            '<link rel="stylesheet" type="text/css" href="https://static.octocolumn.com/static/css/sass/read.css">'
        sub_css = \
            '<link rel="stylesheet" type="text/css" href="https://static.octocolumn.com/static/css/sass/sub.css">'
        response = HttpResponse(read_css + sub_css + contents)
        return response

    def author_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Publish</a>',
            reverse('admin:authorIsActive', args=[obj.pk]),
        )

    def author_draft(self, obj):
        return format_html(
            '<a class="button" href="{}">Draft</a>',
            reverse('admin:authorDraft', args=[obj.pk]),
        )

    def process_is_active(self, request, author_post_pk, *args, **kwargs):
        return self.process_action(
            request=request,
            author_post_pk=author_post_pk,
            action_form=AuthorIsActive,
            action_title='신청완료',
        )

    def process_is_draft(self, request, author_post_pk, *args, **kwargs):
        return self.draft_action(
            request=request,
            author_post_pk=author_post_pk,
            action_form=PostDraftAction,
            action_title='반려',
        )

    def process_action(
            self,
            request,
            author_post_pk,
            action_form,
            action_title
    ):
        author = self.get_object(request, author_post_pk)
        if request.method != 'GET':
            form = action_form()
        else:
            form = action_form(request.POST)
            if form.is_valid():
                if form.save(author):

                    pass
                else:
                    return HttpResponseRedirect(redirect_to='/morningCoffee/column/preauthorpost/')
        return HttpResponseRedirect(redirect_to='/morningCoffee/column/preauthorpost/')

    def draft_action(
            self,
            request,
            author_post_pk,
            action_form,
            action_title
    ):
        author = self.get_object(request, author_post_pk)
        if request.method != 'GET':
            form = action_form()
        else:
            form = action_form(request.POST)
            if form.is_valid():
                if form.save(author):

                    pass
                else:
                    return HttpResponseRedirect(redirect_to='/morningCoffee/column/preauthorpost/')
        return HttpResponseRedirect(redirect_to='/morningCoffee/column/preauthorpost/')

    def remove_tag(self, obj):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', obj)
        return clean_text

    def content_size(self, post):
        clean_text = self.remove_tag(post.main_content)
        return mark_safe('<u>{}</u>글자'.format(len(clean_text)))

    content_size.short_description = '글자수'

    author_actions.shortdescription = '완료'
    author_actions.allow_tags = '완료'
    author_is_active.short_description = '인증 상태'
    author_is_active.admin_order_field = 'author__is_active'
