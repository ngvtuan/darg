# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0007_operator_share_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='share_count',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
