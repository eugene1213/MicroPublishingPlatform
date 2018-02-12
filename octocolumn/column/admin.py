from django.contrib import admin
from django.utils.safestring import mark_safe

from column.models import Post, Temp


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id','author', 'title','created_date','content_size']
    list_display_links = ['id', 'title']
    search_fields = ('author__email',)

    def content_size(self, post):
        return mark_safe('<u>{}</u>글자'.format(len(post.main_content)))

    content_size.short_description = '글자수'


@admin.register(Temp)
class TempAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id','author', 'title','modified_date','content_size']
    list_display_links = ['id', 'title']
    search_fields = ('author__email',)

    def content_size(self, post):
        return mark_safe('<u>{}</u>글자'.format(len(post.main_content)))

    content_size.short_description = '글자수'
# Register your models here.
