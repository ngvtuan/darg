# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0023_auto_20160128_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='is_split',
            field=models.BooleanField(default=False),
        ),
    ]
