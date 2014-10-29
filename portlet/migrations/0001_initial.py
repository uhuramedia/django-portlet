# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portlet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('display_title', models.CharField(default=b'', max_length=255, verbose_name='Displayed title', blank=True)),
                ('display_title_link', models.CharField(default=b'', max_length=255, verbose_name='Displayed title link', blank=True)),
                ('portlet_type', models.SlugField(editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Portlet',
                'verbose_name_plural': 'Portlets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlainTextPortlet',
            fields=[
                ('portlet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='portlet.Portlet')),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'Plain text portlet',
                'verbose_name_plural': 'Plain text portlets',
            },
            bases=('portlet.portlet',),
        ),
        migrations.CreateModel(
            name='ImagePortlet',
            fields=[
                ('portlet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='portlet.Portlet')),
                ('file', models.ImageField(upload_to=b'portletimages')),
                ('alt_text', models.CharField(max_length=255, blank=True)),
                ('link', models.CharField(max_length=255, blank=True)),
                ('classes', models.CharField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=('portlet.portlet',),
        ),
        migrations.CreateModel(
            name='HTMLPortlet',
            fields=[
                ('portlet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='portlet.Portlet')),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'HTML portlet',
                'verbose_name_plural': 'HTML portlets',
            },
            bases=('portlet.portlet',),
        ),
        migrations.CreateModel(
            name='FlashPortlet',
            fields=[
                ('portlet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='portlet.Portlet')),
                ('swf', models.FileField(upload_to=b'portletflash')),
                ('width', models.IntegerField(default=300)),
                ('height', models.IntegerField(default=200)),
                ('flash_vars', models.CharField(default=b'', help_text='clickTAG=http://www.example.com/', max_length=255, blank=True)),
            ],
            options={
            },
            bases=('portlet.portlet',),
        ),
        migrations.CreateModel(
            name='DownloadPortlet',
            fields=[
                ('portlet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='portlet.Portlet')),
                ('file', models.FileField(upload_to=b'portletdownload/', verbose_name='Datei', blank=True)),
                ('image', models.ImageField(upload_to=b'portletdownload', verbose_name='Vorschau Bild')),
                ('text', models.TextField()),
                ('alt_text', models.CharField(max_length=255, blank=True)),
                ('link', models.CharField(max_length=255, blank=True)),
                ('classes', models.CharField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=('portlet.portlet',),
        ),
        migrations.CreateModel(
            name='PortletAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=200, verbose_name='Path')),
                ('inherit', models.BooleanField(default=False, help_text='Inherits this portlet to all sub-paths', verbose_name='Inherit')),
                ('slot', models.CharField(max_length=50, verbose_name='Slot')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='Position')),
                ('prohibit', models.BooleanField(default=False, help_text='Blocks this portlet', verbose_name='Prohibit')),
                ('language', models.CharField(default=b'', choices=[(b'en', b'English'), (b'de', b'Deutsch')], max_length=5, blank=True, verbose_name='Language', db_index=True)),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'Portlet Assignment',
                'verbose_name_plural': 'Portlet Assignments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SnippetPortlet',
            fields=[
                ('portlet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='portlet.Portlet')),
                ('filename', models.CharField(unique=True, max_length=255)),
            ],
            options={
            },
            bases=('portlet.portlet',),
        ),
        migrations.AddField(
            model_name='portletassignment',
            name='portlet',
            field=models.ForeignKey(to='portlet.Portlet'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='portletassignment',
            unique_together=set([('portlet', 'path', 'slot', 'position', 'prohibit', 'language')]),
        ),
    ]
