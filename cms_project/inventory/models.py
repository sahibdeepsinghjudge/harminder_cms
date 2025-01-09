from django.db import models
from django.contrib.auth.models import User
# Create your models here.



device_choices = (('Cable', 'Cable'), ('ONT Single', 'ONT Single'),('ONT Dual', 'ONT Dual'),('Router Single', 'Router Single'),('Router Dual', 'Router Dual'), ('Switch', 'Switch'), ('Other', 'Other'))

class DeviceDetail(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255,null=True,blank=True)
    mac_address = models.CharField(max_length=255,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    units = models.CharField(max_length=255)
    price_per_unit = models.FloatField()
    device_type = models.CharField(max_length=255,choices=device_choices,default='Other')
    in_stock = models.BooleanField(default=True)
    hsn_code = models.CharField(max_length=255,blank=True,null=True)
    image = models.ImageField(upload_to='device_images',blank=True,null=True)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name
    
    def stock_value(self):
        return self.price_per_unit * self.quantity
    


class AttachedDevice(models.Model):
    device = models.ForeignKey(DeviceDetail, on_delete=models.CASCADE)
    date_attached = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    serial_number = models.CharField(max_length=255,null=True,blank=True)
    mac_address = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.device.name

    def stock_value(self):
        return self.device.price_per_unit * self.quantity
    
