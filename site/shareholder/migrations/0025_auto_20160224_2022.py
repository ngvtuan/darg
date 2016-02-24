# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0024_position_is_split'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='founded_at',
            field=models.DateField(default=datetime.datetime(1970, 1, 1, 0, 0), verbose_name='Foundation date of the company'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='operator',
            name='company',
            field=models.ForeignKey(verbose_name=b'Operators Company', to='shareholder.Company'),
        ),
        migrations.AlterField(
            model_name='shareholder',
            name='company',
            field=models.ForeignKey(verbose_name=b'Shareholders Company', to='shareholder.Company'),
        ),
    ]
