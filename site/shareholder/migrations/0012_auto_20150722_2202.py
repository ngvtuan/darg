# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0011_auto_20150623_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='country',
            field=models.ForeignKey(default=0, to='shareholder.Country', help_text='Headquarter location'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
