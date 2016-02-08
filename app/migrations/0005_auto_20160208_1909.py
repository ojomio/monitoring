# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20160208_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='password',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='device',
            name='last_queried',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 8, 19, 8, 45, 500399)),
            preserve_default=True,
        ),
    ]
