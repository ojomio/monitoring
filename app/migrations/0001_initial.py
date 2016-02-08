# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('human_readable', models.CharField(max_length=300)),
                ('ip_address', models.IPAddressField()),
                ('fw_version', models.CharField(max_length=20)),
                ('last_queried', models.DateTimeField(default=datetime.datetime(2016, 2, 8, 18, 26, 5, 51498))),
                ('query_status', models.CharField(choices=[('queue', 'in queue'), ('query', 'querying'), ('success', 'success'), ('failure', 'failure')], max_length=20)),
                ('login', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeviceParams',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('param_name', models.CharField(max_length=1000)),
                ('param_type', models.CharField(choices=[('int', 'int'), ('float', 'float'), ('bool', 'bool'), ('str', 'str'), ('coord', 'coord')], max_length=7)),
                ('param_value', models.CharField(max_length=1000)),
                ('device', models.ForeignKey(related_name='properties', to='app.Device')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
