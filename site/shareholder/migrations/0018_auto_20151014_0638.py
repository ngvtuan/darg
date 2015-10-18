# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from decimal import Decimal
from django.utils.timezone import utc
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0017_optionplan_security'),
    ]

    operations = [
        migrations.AddField(
            model_name='optionplan',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 6, 38, 36, 186545, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='optionplan',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 6, 38, 42, 888542, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='optiontransaction',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 6, 38, 46, 406913, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='optiontransaction',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 6, 38, 48, 646856, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='position',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 6, 38, 53, 20892, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='position',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 6, 38, 56, 13378, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='optionplan',
            name='exercise_price',
            field=models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=4, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]
