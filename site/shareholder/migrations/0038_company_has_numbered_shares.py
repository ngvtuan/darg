# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0037_auto_20160614_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='has_numbered_shares',
            field=models.BooleanField(default=False),
        ),
    ]
