from django.contrib import admin
from django.utils.safestring import mark_safe

from column.models import Post, Temp

import re


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id','author', 'title','created_date','content_size']
    list_display_links = ['id', 'title']
    search_fields = ('author__username',)

    def remove_tag(self, post):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', post)
        return clean_text

    def content_size(self, post):
        clean_text = self.remove_tag(post.main_content)
        return mark_safe('<u>{}</u>글자'.format(len(clean_text)))

    content_size.short_description = '글자수'


@admin.register(Temp)
class TempAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id','author', 'title','modified_date','content_size']
    list_display_links = ['id', 'title']
    search_fields = ('author__username',)

    def remove_tag(self, temp):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', temp)
        return clean_text

    def content_size(self, temp):
        clean_text = self.remove_tag(temp.main_content)
        return mark_safe('<u>{}</u>글자'.format(len(clean_text)))

    content_size.short_description = '글자수'
# Register your models here.
