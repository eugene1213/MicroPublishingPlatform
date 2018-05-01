from django.conf.urls import url

from config.views.support import index, notice, policies, help_octo, contact, staff_blog, jobs

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^notice/$', notice, name='notice'),
    url(r'^policies/', policies, name='policies'),
    url(r'^notice/$', help_octo, name='notice'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^staffBlog/$', staff_blog, name='staffBlog'),
    url(r'^help/$', help_octo, name='staffBlog'),
    url(r'^jobs/$', jobs, name='staffBlog'),

]