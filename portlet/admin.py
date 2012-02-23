from django.contrib import admin
from portlet.models import HTMLPortlet, Portlet, PortletAssignment, \
    PlainTextPortlet, ImagePortlet

class PortletAssignmentInline(admin.TabularInline):
    model = PortletAssignment

class PortletAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [PortletAssignmentInline]
admin.site.register(Portlet, PortletAdmin)

class HTMLPortletAdmin(PortletAdmin):
    pass
admin.site.register(HTMLPortlet, HTMLPortletAdmin)

class PlainTextPortletAdmin(PortletAdmin):
    pass
admin.site.register(PlainTextPortlet, PlainTextPortletAdmin)

class ImagePortletAdmin(PortletAdmin):
    pass
admin.site.register(ImagePortlet, ImagePortletAdmin)
