from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.importlib import import_module
from portlet.models import HTMLPortlet, Portlet, PortletAssignment, \
    PlainTextPortlet, ImagePortlet, FlashPortlet, SnippetPortlet, DownloadPortlet


def get_class_from_string(str):
    path = str
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    try:
        mod = import_module(module)
        return getattr(mod, attr)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' % (module, e))


class PortletAssignmentInline(admin.TabularInline):
    extra = 0
    model = PortletAssignment

class PortletAdmin(admin.ModelAdmin):
    list_display = ('title', 'portlet_type', 'display_title', 'created', 'modified', 'is_assigned')
    ordering = ('title',)
    inlines = [PortletAssignmentInline]
    search_fields = ('title', 'display_title')
    actions = ('update_type',)

    def update_type(self, request, queryset):
        for obj in queryset:
            obj.update_type()
            obj.save()


class PortletEditorAdmin(PortletAdmin):
    """
    This admin comes with an optional editor that you can set in the settings
    """
    def __init__(self, *args, **kwargs):
        super(PortletAdmin, self).__init__(*args, **kwargs)
        setting = "PORTLET_TEXTWIDGET"
        if hasattr(settings, setting):
            self.formfield_overrides = {
                models.TextField: {'widget': get_class_from_string(getattr(settings, setting)) }
            }

class PortletMasterAdmin(PortletAdmin):
    def has_add_permission(self, request):
        return False
admin.site.register(Portlet, PortletMasterAdmin)

class HTMLPortletAdmin(PortletEditorAdmin):
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

admin.site.register(DownloadPortlet, PortletAdmin)
