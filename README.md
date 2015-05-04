# django-portlet
Django portlets (Server side rendering of ui blocks)

Install
=======

`pip install git+git://github.com/uhuramedia/django-portlet.git`

Usage
=====

1. Include `portlet` in INSTALLED_APPS
2. Add url `url(r'^portlet/', include('portlet.urls'))` to projet urls.py
3. Use slot template tag to add portlets in template

`{% load portlet_tags %}`

`{% slot 'slot_name' %}`


