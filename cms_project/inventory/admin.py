from django.contrib import admin
from .models import DeviceDetail,ProviderCompanies,AttachedDevice
# Register your models here.


admin.site.register(DeviceDetail)
admin.site.register(ProviderCompanies)
admin.site.register(AttachedDevice)