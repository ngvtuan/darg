# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0018_auto_20151014_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optionplan',
            name='count',
            field=models.PositiveIntegerField(help_text='Anzahl der genehmigten Aktien'),
        ),
    ]
