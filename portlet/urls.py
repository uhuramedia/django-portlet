from django.conf.urls import *
from .views import *

urlpatterns = [
    url(r'^delete/(\d+)/$', delete),
    url(r'^inherit/(\d+)/$', inherit),
    url(r'^add/$', add),
    url(r'^moveup/(\d+)/$', moveup),
    url(r'^movedown/(\d+)/$', movedown),
    url(r'^move/(\d+)/(-?\d+)/(.+)/$', move),
]