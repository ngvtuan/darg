# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0038_company_has_numbered_shares'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='has_numbered_shares',
        ),
        migrations.AddField(
            model_name='security',
            name='has_numbered_shares',
            field=models.BooleanField(default=False, verbose_name='Shareholders have security IDs assigned.'),
        ),
    ]
