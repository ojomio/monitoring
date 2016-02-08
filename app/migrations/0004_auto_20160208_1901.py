# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20160208_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='last_queried',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 8, 19, 1, 7, 920274)),
            preserve_default=True,
        ),
    ]
