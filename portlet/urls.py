from django.conf.urls import patterns

urlpatterns = patterns('portlet.views',
    (r'^delete/(\d+)/$', 'delete'),
    (r'^inherit/(\d+)/$', 'inherit'),
    (r'^add/$', 'add'),
    (r'^moveup/(\d+)/$', 'moveup'),
    (r'^movedown/(\d+)/$', 'movedown'),
    (r'^move/(\d+)/(-?\d+)/(.+)/$', 'move'),
)
