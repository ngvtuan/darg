# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0016_optionplan_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='optionplan',
            name='security',
            field=models.ForeignKey(default=None, to='shareholder.Security'),
            preserve_default=False,
        ),
    ]
