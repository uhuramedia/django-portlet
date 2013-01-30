import simplejson

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from portlet.models import PortletAssignment, Portlet
from django.shortcuts import get_object_or_404
from django.utils import translation


@user_passes_test(lambda u: u.is_staff)
def inherit(request, pk):
    """ delete a portlet assignment """
    try:
        a = get_object_or_404(PortletAssignment, pk=pk)
        a.inherit = not a.inherit
        a.save()
        return HttpResponse('')
    except Exception, e:
        return HttpResponse("Error: " + str(e))


@user_passes_test(lambda u: u.is_staff)
def delete(request, pk):
    """ delete a portlet assignment """
    where = request.GET.get('where', '')
    path = request.GET.get('path', '')
    try:
        a = get_object_or_404(PortletAssignment, pk=pk)
        if path != "" and where == "here":
            a.path = path
            a.inherit = False
            a.pk = None
            a.prohibit = True
            a.save()
        elif path != "" and where == "here-inherit":
            a.path = path
            a.inherit = True
            a.pk = None
            a.prohibit = True
            a.save()
        else:
            a.delete()
        return HttpResponse('')
    except Exception, e:
        return HttpResponse("Error: " + str(e))


@user_passes_test(lambda u: u.is_staff)
@csrf_exempt
def add(request):
    if request.GET.has_key('pk'):
        path = request.GET.get('path')
        pk = request.GET.get('pk')
        slot = request.GET.get('slot')
        #lang = translation.get_language()
        a = PortletAssignment(path=path, portlet_id=pk, slot=slot)
        a.save()
        return HttpResponseRedirect(path)
    else:
        portlet_list = Portlet.objects.order_by("portlet_type", "title")
        data = {}
        for p in portlet_list:
            if not data.has_key(p.portlet_type):
                data[p.portlet_type] = []
            data[p.portlet_type].append({'title': p.title, 'pk': p.pk})
        data = [ {'category': k, 'portlets': v} for k, v in data.items()]
        data.sort(lambda x, y: cmp(len(y['portlets']), len(x['portlets'])))
        return HttpResponse(simplejson.dumps(data))


@user_passes_test(lambda u: u.is_staff)
@csrf_exempt
def change(request):
    if request.method == "POST":
        content = request.POST.get("content", "")
        element = request.POST.get("element", "")
        pk = element.replace("portlet-content-", "")
        p = Portlet.objects.get(pk=pk).get_object()
        p.text = content
        p.save()
        print p, content
        return HttpResponse("OK")
    return HttpResponse("")

@user_passes_test(lambda u: u.is_staff)
def moveup(request, pk):
    assignment = get_object_or_404(PortletAssignment, pk=pk)
    assignment.move_up()
    return HttpResponse(assignment.position)


@user_passes_test(lambda u: u.is_staff)
def movedown(request, pk):
    assignment = get_object_or_404(PortletAssignment, pk=pk)
    assignment.move_down()
    return HttpResponse(assignment.position)


@user_passes_test(lambda u: u.is_staff)
def move(request, pk, delta, slot):
    assignment = get_object_or_404(PortletAssignment, pk=pk)
    assignment.slot = slot
    assignment.move(int(delta))
    return HttpResponse(assignment.position)
