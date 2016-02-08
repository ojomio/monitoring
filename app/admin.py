from django.contrib import admin
# Register your models here.
from django.contrib.admin.options import ModelAdmin, StackedInline

from app.models import Device, DeviceParams


class DeviceParamInline(StackedInline):
    model = DeviceParams
    extra = 1


class DeviceAdmin(ModelAdmin):
    inlines = [DeviceParamInline]
    list_display = ['__str__', 'fw_version', 'last_queried','is_active', 'query_status']
    list_editable = ['is_active']
    list_filter = ['is_active']

    readonly_fields = ['last_queried','fw_version']


admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceParams)
