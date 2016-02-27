# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0028_auto_20160226_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='buyer',
            field=models.ForeignKey(related_name='buyer', blank=True, to='shareholder.Shareholder', null=True),
        ),
    ]
