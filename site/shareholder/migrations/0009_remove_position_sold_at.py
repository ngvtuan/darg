# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0008_company_share_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='sold_at',
        ),
    ]
