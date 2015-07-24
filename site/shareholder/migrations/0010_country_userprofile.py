# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shareholder', '0009_remove_position_sold_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('iso_code', models.CharField(max_length=2, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'ordering': ['name', 'iso_code'],
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.TextField()),
                ('city', models.TextField()),
                ('province', models.TextField(null=True)),
                ('postal_code', models.TextField()),
                ('country', models.ForeignKey(to='shareholder.Country')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]
