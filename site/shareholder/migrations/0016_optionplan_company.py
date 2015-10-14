# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0015_auto_20150920_0520'),
    ]

    operations = [
        migrations.AddField(
            model_name='optionplan',
            name='company',
            field=models.ForeignKey(default=None, to='shareholder.Company'),
            preserve_default=False,
        ),
    ]
