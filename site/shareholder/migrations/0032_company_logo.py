# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import shareholder.models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0031_optiontransaction_is_draft'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ImageField(null=True, upload_to=shareholder.models.get_company_logo_upload_path, blank=True),
        ),
    ]
