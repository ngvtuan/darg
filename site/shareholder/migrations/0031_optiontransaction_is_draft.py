# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0030_position_is_draft'),
    ]

    operations = [
        migrations.AddField(
            model_name='optiontransaction',
            name='is_draft',
            field=models.BooleanField(default=True),
        ),
    ]
