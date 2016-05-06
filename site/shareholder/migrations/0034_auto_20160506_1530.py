# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0033_auto_20160506_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='ip',
            field=models.GenericIPAddressField(null=True, blank=True),
        ),
    ]
