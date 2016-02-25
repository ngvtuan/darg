# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0026_auto_20160224_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='provisioned_capital',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='count',
            field=models.PositiveIntegerField(verbose_name='Share Count transfered or created'),
        ),
        migrations.AlterField(
            model_name='position',
            name='value',
            field=models.DecimalField(null=True, verbose_name='Nominal value or payed price for the transaction', max_digits=8, decimal_places=4, blank=True),
        ),
    ]
