# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0005_auto_20150418_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='value',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=4, blank=True),
        ),
    ]
