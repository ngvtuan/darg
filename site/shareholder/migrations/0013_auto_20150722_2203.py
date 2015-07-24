# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0012_auto_20150722_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='country',
            field=models.ForeignKey(to='shareholder.Country', help_text='Headquarter location', null=True),
        ),
    ]
