# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(null=True, upload_to=api.models._profile_photo_upload_to, blank=True),
            preserve_default=True,
        ),
    ]
