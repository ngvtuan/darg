# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import shareholder.models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0020_auto_20151026_0301'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name_plural': 'UserProfile'},
        ),
        migrations.AddField(
            model_name='position',
            name='comment',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='optionplan',
            name='pdf_file',
            field=models.FileField(null=True, upload_to=shareholder.models.get_option_plan_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='company_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='province',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='street',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
