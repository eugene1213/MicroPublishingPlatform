from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from rest_framework.authtoken.models import Token

from member.models import User, Author

admin.site.unregister(Site)
admin.site.unregister(Group)
admin.site.unregister(Token)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name','last_name','point']
    list_display_links = ['email']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['author', 'is_active','created_at']
    list_display_links = ['author']



# Register your models here.
