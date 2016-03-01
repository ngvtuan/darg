# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0029_auto_20160227_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='is_draft',
            field=models.BooleanField(default=True),
        ),
    ]
