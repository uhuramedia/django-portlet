from django.contrib import admin
from portlet.models import HTMLPortlet, Portlet, PortletAssignment

class PortletAssignmentInline(admin.TabularInline):
    model = PortletAssignment

class PortletAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [PortletAssignmentInline]
admin.site.register(Portlet, PortletAdmin)

class HTMLPortletAdmin(PortletAdmin):
    pass
admin.site.register(HTMLPortlet, HTMLPortletAdmin)
