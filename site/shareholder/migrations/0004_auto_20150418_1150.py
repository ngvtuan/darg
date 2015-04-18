# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0003_position_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='shareholder',
        ),
        migrations.AddField(
            model_name='position',
            name='buyer',
            field=models.ForeignKey(related_name='buyer', default=0, to='shareholder.Shareholder'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='position',
            name='seller',
            field=models.ForeignKey(related_name='seller', blank=True, to='shareholder.Shareholder', null=True),
        ),
    ]
