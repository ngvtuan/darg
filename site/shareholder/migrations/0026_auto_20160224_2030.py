# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0025_auto_20160224_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='founded_at',
            field=models.DateField(null=True, verbose_name='Foundation date of the company'),
        ),
    ]
