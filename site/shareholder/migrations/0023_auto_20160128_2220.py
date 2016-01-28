# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0022_auto_20160128_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.ForeignKey(to='shareholder.Country', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='postal_code',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
