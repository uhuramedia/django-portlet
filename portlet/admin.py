from django.contrib import admin
from portlet.models import HTMLPortlet, Portlet, PortletAssignment, \
    PlainTextPortlet, ImagePortlet, FlashPortlet, SnippetPortlet

class PortletAssignmentInline(admin.TabularInline):
    extra = 0
    model = PortletAssignment

class PortletAdmin(admin.ModelAdmin):
    list_display = ('title', 'portlet_type', 'display_title', 'created', 'modified', 'is_assigned')
    ordering = ('title',)
    inlines = [PortletAssignmentInline]
    actions = ('update_type',)

    def update_type(self, request, queryset):
        for obj in queryset:
            obj.update_type()
            obj.save()


class PortletMasterAdmin(PortletAdmin):
    def has_add_permission(self, request):
        return False
admin.site.register(Portlet, PortletMasterAdmin)

class HTMLPortletAdmin(PortletAdmin):
    pass
admin.site.register(HTMLPortlet, HTMLPortletAdmin)

class PlainTextPortletAdmin(PortletAdmin):
    pass
admin.site.register(PlainTextPortlet, PlainTextPortletAdmin)

class ImagePortletAdmin(PortletAdmin):
    pass
admin.site.register(ImagePortlet, ImagePortletAdmin)

admin.site.register(FlashPortlet, PortletAdmin)

admin.site.register(SnippetPortlet, PortletAdmin)
