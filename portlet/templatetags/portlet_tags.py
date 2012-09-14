from colorsys import hsv_to_rgb
from django import template
from django.utils import translation
from hashlib import md5
from portlet.models import PortletAssignment

register = template.Library()

@register.inclusion_tag('portlet/slot.html', takes_context=True)
def slot(context, slot_name, path_override=None, extra=None):
    request = context.get('request')
    lang = translation.get_language()
    if extra and str(extra) != "":
        slot_name = "-".join((slot_name, str(extra)))
    if path_override:
        path = path_override
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
    hexstring = md5((name).encode('latin1', 'replace')).hexdigest()[:2]
    floatcolor = int("0x" + hexstring, 16) / 255.0
    h = floatcolor # Select random green'ish hue from hue wheel
    s = 0.6
    v = 1
    r, g, b = hsv_to_rgb(h, s, v)
    return "".join([hex(int(x * 255)).replace("0x", "").rjust(2, "0") for x in (r, g, b)])

def get_contrast_color(hexcolor):
    hexcolor = int("0x" + hexcolor, 16)
    if hexcolor > 0xffffff / 1.5:
        return "000000"
    return "FFFFFF"
