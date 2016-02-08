# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20160208_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='fw_version',
            field=models.CharField(max_length=20, verbose_name='Версия прошивки', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='human_readable',
            field=models.CharField(max_length=300, verbose_name='Идентификатор'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='is_active',
            field=models.BooleanField(verbose_name='Активен', default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='last_queried',
            field=models.DateTimeField(verbose_name='Время последнего опроса', default=datetime.datetime(2016, 2, 8, 21, 30, 42, 49201)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='query_status',
            field=models.CharField(max_length=20, verbose_name='Результат опроса', default='queue', choices=[('queue', 'В очереди'), ('query', 'Опрашивается'), ('success', 'Успех'), ('failure', 'Ошибка')], blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='deviceparams',
            name='param_type',
            field=models.CharField(max_length=7, default='str', choices=[('int', 'int'), ('float', 'float'), ('bool', 'bool'), ('str', 'str'), ('coord', 'coord')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='deviceparams',
            name='param_value',
            field=models.CharField(max_length=1000, blank=True),
            preserve_default=True,
        ),
    ]
