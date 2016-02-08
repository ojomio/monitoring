# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160208_1831'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='device',
            options={'verbose_name': 'Устройство', 'verbose_name_plural': 'Устройства'},
        ),
        migrations.AlterModelOptions(
            name='deviceparams',
            options={'verbose_name': 'Параметр конфигурации', 'verbose_name_plural': 'Параметры конфигурации'},
        ),
        migrations.AlterField(
            model_name='device',
            name='last_queried',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 8, 18, 53, 1, 797726)),
            preserve_default=True,
        ),
    ]
