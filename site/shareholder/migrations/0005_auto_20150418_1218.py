# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0004_auto_20150418_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='sold_at',
            field=models.DateField(null=True, blank=True),
        ),
    ]
