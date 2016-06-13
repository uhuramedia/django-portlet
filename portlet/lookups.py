# -*- coding: utf-8 -*-

from ajax_select import register, LookupChannel
try:
    from HavelCMS.models import Page
except:
    pass

@register('pages')
class PageLookup(LookupChannel):

    model = Page

    def get_query(self, q, request):
        qs = self.model.objects.filter(title__icontains=q).order_by('title')[:50]
        return qs

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.title

    def get_result(self, obj):
        return obj.get_absolute_url()
