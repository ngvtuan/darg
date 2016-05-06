# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0032_company_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='ip',
            field=models.GenericIPAddressField(default='0.0.0.0'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='tnc_accepted',
            field=models.BooleanField(default=False),
        ),
    ]
