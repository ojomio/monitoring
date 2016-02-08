# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='last_queried',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 8, 18, 31, 44, 462597)),
            preserve_default=True,
        ),
    ]
