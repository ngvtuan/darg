# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0027_auto_20160225_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='founded_at',
            field=models.DateField(null=True, verbose_name='Gr\xfcndungsdatum des Unternehmens'),
        ),
        migrations.AlterField(
            model_name='position',
            name='count',
            field=models.PositiveIntegerField(verbose_name='transferierte oder erstellte Aktienanzahl'),
        ),
        migrations.AlterField(
            model_name='position',
            name='value',
            field=models.DecimalField(null=True, verbose_name='Nominalwert (bei Kapitalerh\xf6hung) oder Kaufpreis', max_digits=8, decimal_places=4, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.ForeignKey(blank=True, to='shareholder.Country', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
