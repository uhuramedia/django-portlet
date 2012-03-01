import datetime

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.template import loader, Context
from django.template.defaultfilters import slugify
from django.core import urlresolvers
from django.db.models.fields.related import SingleRelatedObjectDescriptor
from django.conf import settings

class Portlet(models.Model):
    template = 'portlet/base.html'
    title = models.CharField(max_length=100)
    display_title = models.CharField(max_length=255, blank=True, default="")
    portlet_type = models.SlugField(editable=False)
    created = models.DateTimeField(default=datetime.datetime.now, editable=False)
    modified = models.DateTimeField(auto_now=True, default=datetime.datetime.now, editable=False)

    def slug(self, lang=None):
        return slugify(self.title)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.portlet_type:
            self.portlet_type = self.__class__.__name__
        super(Portlet, self).save(*args, **kwargs)

    def update(self, request):
        self.request = request

    def render(self):
        t = loader.get_template(self.__template__)
        c = Context({'portlet': self, 'request': self.request})
        return t.render(c)

    def get_object(self):
        return getattr(self, self.portlet_type.lower())
    
    def get_edit_link(self):
        # reverse admin url to get link to specific object
        return urlresolvers.reverse('admin:%s_%s_change' % (self._meta.app_label,
                                                            self.portlet_type.lower()),
                                    args=(self.pk,))
    
    @staticmethod
    def select_subclasses(*subclasses):
        if not subclasses:
            subclasses = Portlet.get_subclasses()
        new_qs = Portlet.objects.all().select_related(*subclasses)
        new_qs.subclasses = subclasses
        return new_qs

    @staticmethod
    def get_subclasses():
        return [o for o in dir(Portlet)
                      if isinstance(getattr(Portlet, o), SingleRelatedObjectDescriptor)\
                      and issubclass(getattr(Portlet,o).related.model, Portlet)]

    class Meta:
        verbose_name = _('Portlet')
        verbose_name_plural = _('Portlets')


def split_path(path):
    """
    "/a/b/c/" => ['/a/b/c/', '/a/b/', '/a/', '/']
    "/" => ['/']
    """
    result = []
    listpath = path.strip("/").split("/")
    while len(listpath) > 0 and listpath != [""]:
        result.append("/%s/" % "/".join(listpath))
        listpath.pop()
    result.append("/")
    return result
        

class PortletAssignment(models.Model):
    portlet = models.ForeignKey(Portlet)
    path = models.CharField(max_length=200)
    inherit = models.BooleanField(default=False, help_text="Inherits this portlet to all sub-paths")
    slot = models.SlugField()
    position = models.PositiveIntegerField(default=0)
    prohibit = models.BooleanField(default=False, help_text="Blocks this portlet")
    language = models.CharField(max_length=5, db_index=True, blank=True,
                                choices=settings.LANGUAGES, 
                                default=settings.LANGUAGES[0][0])
    
    def __unicode__(self):
        return u"[%s] %s (%s) @ %s" % (self.portlet, self.slot, self.position, self.path)
    
    def move_up(self):
        return self.move(-1)
    
    def move_down(self):
        return self.move(1)
    
    def move(self, delta):
        # there is always just one portlet at one position, so if the position
        # we want is already taken, we swap
        desired_position = self.position+delta
        if desired_position < 0:
            return
        old_position = self.position
        conflict = False
        try:
            pa = PortletAssignment.objects.get(path=self.path, slot=self.slot,
                                               position=desired_position)
            conflict = True
            pa.position = 444
            pa.save()
        except PortletAssignment.DoesNotExist:
            pass
        self.position = desired_position
        self.save()
        if conflict:
            pa.position = old_position
            pa.save()
            
    @staticmethod
    def move_path(old, new, keep_old=False):
        assignments = PortletAssignment.objects.filter(path__startswith=old)
        for assignment in assignments:
            assignment.path = assignment.path.replace(old, new)
            if keep_old:
                assignment.pk = None
            assignment.save()
    
    @staticmethod
    def get_for_path(path, slot, language):
        """ get all assigned portlets for path"""
        path = split_path(path)
        query = Q(path=path.pop(0))
        for p in path:
            # for other parts of path, check if there are inherited portlets
            query |= Q(path=p,
                       inherit=True)
        return PortletAssignment.objects.filter(query).\
            filter(slot=slot).filter(Q(language=language) | Q(language="")).\
            select_related(*["portlet__%s" % s for s in Portlet.get_subclasses()]).\
            order_by('-prohibit', 'position', '-path')

    class Meta:
        verbose_name = _('Portlet Assignment')
        verbose_name_plural = _('Portlet Assignments')
        ordering = ('position',)
        unique_together = ('portlet', 'path', 'slot', 'position', 'prohibit', 'language')


class HTMLPortlet(Portlet):
    template = 'portlet/html.html'
    text = models.TextField()

    class Meta:
        verbose_name = _('HTML Portlet')
        verbose_name_plural = _('HTML Portlets')


class PlainTextPortlet(Portlet):
    template = 'portlet/text.html'
    text = models.TextField()

    class Meta:
        verbose_name = _('Text Portlet')
        verbose_name_plural = _('Text Portlets')
        
class ImagePortlet(Portlet):
    template = 'portlet/image.html'
    file = models.ImageField(upload_to="portletimages")
    alt_text = models.CharField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    classes = models.CharField(max_length=255, blank=True)
