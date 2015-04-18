# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0002_operator'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='value',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=4),
            preserve_default=False,
        ),
    ]
