# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0019_auto_20151026_0159'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='security',
            field=models.ForeignKey(default=0, to='shareholder.Security'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='security',
            name='company',
            field=models.ForeignKey(default=0, to='shareholder.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='security',
            name='count',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
