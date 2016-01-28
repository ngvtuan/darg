# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0021_auto_20160128_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='comment',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
