# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0036_auto_20160512_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='value',
            field=models.DecimalField(null=True, verbose_name='Nominalwert (bei Kapitalerh\xf6hung) oder Kaufpreis', max_digits=16, decimal_places=8, blank=True),
        ),
    ]
