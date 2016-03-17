import datetime

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.template import loader, Context
from django.template.defaultfilters import slugify
from django.core import urlresolvers
from django.conf import settings
from django.utils import translation
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor

class Portlet(models.Model):
    template = 'portlet/base.html'
    title = models.CharField(_("Title"), max_length=100)
    display_title = models.CharField(_("Displayed title"), max_length=255, blank=True, default="")
    display_title_link = models.CharField(_("Displayed title link"), max_length=255, blank=True, default="")
    portlet_type = models.SlugField(editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def slug(self, lang=None):
        return slugify(self.title)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.portlet_type:
            self.portlet_type = self.__class__.__name__
        super(Portlet, self).save(*args, **kwargs)

    def update_type(self):
        self.portlet_type = self.__class__.__name__

    def update(self, request):
        self.request = request

    def render(self):
        t = loader.get_template(self.__template__)
        c = Context({'portlet': self, 'request': self.request})
        return t.render(c)

    def vary_on(self):
        """
        Used in template cache tag.
        Use variables on which the portlet content does vary.
        ID and modification time (for cache busting!) are hardcoded in template

        Override like this:
            return (super(YOURPortletClass, self).vary_on() +
                   [self.request.blah, self.blah])
        """
        return [translation.get_language()]

    def get_object(self):
        return getattr(self, self.portlet_type.lower())

    def get_edit_link(self):
        # reverse admin url to get link to specific object
        return urlresolvers.reverse('admin:%s_%s_change' % (self._meta.app_label,
                                                            self.portlet_type.lower()),
                                    args=(self.pk,))

    def is_assigned(self):
        return self.portletassignment_set.all().count() > 0

    is_assigned.boolean = True

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
                      if isinstance(getattr(Portlet, o), ReverseOneToOneDescriptor)\
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
    path = models.CharField(_("Path"), max_length=200, db_index=True)
    inherit = models.BooleanField(_("Inherit"), default=False, help_text=_("Inherits this portlet to all sub-paths"))
    slot = models.CharField(_("Slot"), max_length=50, db_index=True)
    position = models.PositiveIntegerField(_("Position"), default=0)
    prohibit = models.BooleanField(_("Prohibit"), default=False, help_text=_("Blocks this portlet"))
    language = models.CharField(_("Language"), max_length=5, db_index=True, blank=True,
                                choices=settings.LANGUAGES,
                                default="")# settings.LANGUAGES[0][0])

    def __unicode__(self):
        return u"[%s] %s (%s) @ %s" % (self.portlet, self.slot, self.position, self.path)

    def save(self, *args, **kwargs):
        if self.pk is None and self.position == 0:
            self.position = PortletAssignment.objects.filter(path=self.path, slot=self.slot).count()
        super(PortletAssignment, self).save(*args, **kwargs)

    def move_up(self):
        return self.move(-1)

    def move_down(self):
        return self.move(1)

    def move(self, delta):
        # there is always just one portlet at one position, so if the position
        # we want is already taken, we swap
        desired_position = self.position+delta
        if desired_position < 0:
            desired_position = 0
        old_position = self.position
        conflict = False
        pa = PortletAssignment.objects.filter(path=self.path, slot=self.slot,
                                              position=desired_position)
        if pa.count() > 0:
            conflict = True
            for p in pa:
                p.position = 444
                p.save()
        self.position = desired_position
        self.save()
        if conflict:
            for p in pa:
                p.position = old_position
                p.save()
        PortletAssignment.clean_order(self.path, self.slot)

    @staticmethod
    def clean_order(path=path, slot=slot):
        assignments = PortletAssignment.objects.filter(path=path, slot=slot).\
                          order_by('-prohibit', 'position', '-path')
        i = 0
        for assignment in assignments:
            assignment.position = i
            assignment.save()
            i += 1

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
        verbose_name = _('HTML portlet')
        verbose_name_plural = _('HTML portlets')


class PlainTextPortlet(Portlet):
    template = 'portlet/text.html'
    text = models.TextField()

    class Meta:
        verbose_name = _('Plain text portlet')
        verbose_name_plural = _('Plain text portlets')


class SnippetPortlet(Portlet):
    filename = models.CharField(max_length=255, unique=True)

    @property
    def template(self):
        return "portlet/snippet/%s" % self.filename


class ImagePortlet(Portlet):
    template = 'portlet/image.html'
    file = models.ImageField(upload_to="portletimages")
    alt_text = models.CharField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    classes = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = _('Image portlet')
        verbose_name_plural = _('Image portlets')


class FlashPortlet(Portlet):
    template = 'portlet/flash.html'
    swf = models.FileField(upload_to="portletflash")
    width = models.IntegerField(default=300)
    height = models.IntegerField(default=200)
    flash_vars = models.CharField(help_text=u"clickTAG=http://www.example.com/", max_length=255, blank=True, default="")

    class Meta:
        verbose_name = _('Flash portlet')
        verbose_name_plural = _('Flash portlets')


class DownloadPortlet(Portlet):
    template = 'portlet/download.html'
    file = models.FileField(_('Datei'), upload_to='portletdownload/', blank=True)
    image = models.ImageField(_('Vorschau Bild'), upload_to="portletdownload")
    text = models.TextField()
    alt_text = models.CharField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    classes = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = _('Download portlet')
        verbose_name_plural = _('Download portlets')

