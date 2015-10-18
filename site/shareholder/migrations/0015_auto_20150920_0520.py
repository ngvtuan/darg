# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0014_auto_20150726_2305'),
    ]

    operations = [
        migrations.CreateModel(
            name='OptionPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('board_approved_at', models.DateField()),
                ('title', models.CharField(max_length=255)),
                ('exercise_price', models.DecimalField(null=True, max_digits=8, decimal_places=4, blank=True)),
                ('count', models.PositiveIntegerField(help_text='Number of shares approved')),
                ('comment', models.TextField(null=True, blank=True)),
                ('pdf_file', models.FileField(null=True, upload_to=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OptionTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bought_at', models.DateField()),
                ('count', models.PositiveIntegerField()),
                ('vesting_months', models.PositiveIntegerField(null=True, blank=True)),
                ('buyer', models.ForeignKey(related_name='option_buyer', to='shareholder.Shareholder')),
                ('option_plan', models.ForeignKey(to='shareholder.OptionPlan')),
                ('seller', models.ForeignKey(related_name='option_seller', blank=True, to='shareholder.Shareholder', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Security',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1, choices=[(b'P', b'Preferred Stock'), (b'C', b'Common Stock')])),
            ],
        ),
        migrations.AlterField(
            model_name='company',
            name='share_count',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='operator',
            name='share_count',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='count',
            field=models.PositiveIntegerField(),
        ),
    ]
