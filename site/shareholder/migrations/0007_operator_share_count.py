# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0006_auto_20150418_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='operator',
            name='share_count',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
