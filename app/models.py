import datetime
from django.db import models
from django.db.models.fields import CharField, IPAddressField, DateTimeField, BooleanField
from django.db.models.fields.related import ForeignKey


class Device(models.Model):
    human_readable = CharField(max_length=300, verbose_name='Идентификатор')
    is_active = BooleanField(default=True, verbose_name='Активен')
    ip_address = IPAddressField()
    fw_version = CharField(max_length=20, blank=True, verbose_name='Версия прошивки')
    last_queried = DateTimeField(default=datetime.datetime.now(), verbose_name='Время последнего опроса')
    query_status = CharField(max_length=20, blank=True, default='queue', verbose_name='Результат опроса',
                             choices=[('queue', 'В очереди'), ('query', 'Опрашивается'), ('success', 'Успех'),
                                      ('failure', 'Ошибка')])

    login = CharField(max_length=200)
    password = CharField(max_length=128)


    class Meta:
        verbose_name = u'Устройство'
        verbose_name_plural = u'Устройства'

    def __str__(self):
        return '%s@%s' % (self.human_readable, self.ip_address)


class DeviceParams(models.Model):
    device = ForeignKey(Device, 'id', related_name='properties')
    param_name = CharField(max_length=1000, null=False)
    param_type = CharField(max_length=7,
                           choices=[('int', 'int'), ('float', 'float'), ('bool', 'bool'), ('str', 'str'),
                                    ('coord', 'coord')], null=False, default='str')
    param_value = CharField(max_length=1000, blank=True)

    class Meta:
        verbose_name = u'Параметр конфигурации'
        verbose_name_plural = u'Параметры конфигурации'
