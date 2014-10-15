import django

if django.get_version() >= '1.5':
    from django.conf.urls import *
else:
    from django.conf.urls.defaults import *

urlpatterns = patterns('portlet.views',
    (r'^delete/(\d+)/$', 'delete'),
    (r'^inherit/(\d+)/$', 'inherit'),
    (r'^add/$', 'add'),
    (r'^moveup/(\d+)/$', 'moveup'),
    (r'^movedown/(\d+)/$', 'movedown'),
    (r'^move/(\d+)/(-?\d+)/(.+)/$', 'move'),
)
