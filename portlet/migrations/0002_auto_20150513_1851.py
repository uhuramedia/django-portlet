# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portlet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portletassignment',
            name='path',
            field=models.CharField(max_length=200, verbose_name='Path', db_index=True),
        ),
        migrations.AlterField(
            model_name='portletassignment',
            name='slot',
            field=models.CharField(max_length=50, verbose_name='Slot', db_index=True),
        ),
    ]
