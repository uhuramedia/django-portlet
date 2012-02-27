from django import template
from django.utils import translation
from portlet.models import PortletAssignment

register = template.Library()

@register.inclusion_tag('portlet/slot.html', takes_context=True)
def slot(context, slot_name, path_override=None, path_extra=None):
    request = context.get('request')
    lang = translation.get_language()
    if path_override:
        path = path_override
        if path_extra:
            path = path + path_extra
    else:
        path = request.path

    assignments = PortletAssignment.get_for_path(path=path, slot=slot_name, language=lang)

    portlets = []
    blocklist = []
    for a in assignments:
        if a.prohibit:
            blocklist.append(a.portlet.pk)
            continue
        portlet = a.portlet.get_object()
        portlet.update(request)
        portlet.assignment = a
        portlet.prohibited = portlet.pk in blocklist
        portlets.append(portlet)
        
    return {'portlets': portlets, 'slot_name': slot_name, 'request': request}
