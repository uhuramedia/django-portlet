from django import template
from django.utils import translation
from portlet.models import PortletAssignment
from hashlib import md5

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
        
    hex = get_color(slot_name)
    color = {'background': hex, 'contrast': get_contrast_color(hex)}

    return {'portlets': portlets, 'slot_name': slot_name, 'request': request,
            'color': color}


def get_color(name):
    return md5((name).encode('latin1', 'replace')).hexdigest()[:6]

def get_contrast_color(hexcolor):
    hexcolor = int("0x" + hexcolor, 16)
    if hexcolor > 0xffffff / 2:
        return "000000"
    return "FFFFFF"
