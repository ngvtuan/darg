# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0039_auto_20160720_1044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='security',
            name='has_numbered_shares',
        ),
        migrations.AddField(
            model_name='security',
            name='track_numbers',
            field=models.BooleanField(default=False, verbose_name='App needs to track IDs of shares'),
        ),
    ]
