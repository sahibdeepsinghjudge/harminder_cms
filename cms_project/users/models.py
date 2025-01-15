from django.db import models
from django.contrib.auth.models import User
from complaints.models import Complaint
from django.utils.crypto import get_random_string
from datetime import timedelta
from django.utils import timezone
# Create your models here.

class Partner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    area = models.TextField()
    phone = models.CharField(max_length=15)
    addhar_number = models.TextField()
    pan_number = models.TextField()

    def __str__(self):
        return self.user.username
    

    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255,null=True,blank=True)
    state = models.CharField(max_length=255,null=True,blank=True)
    zip_code = models.CharField(max_length=10,null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    addhar_number = models.TextField(null=True,blank=True)
    pan_number = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    customer_id = models.CharField(max_length=255,default='0')
    date_joined = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)    
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, blank=True, null=True)
    devices = models.ManyToManyField('inventory.AttachedDevice', blank=True,null=True)


    def __str__(self):
        return self.user.username
    

    def save(self, *args, **kwargs):
        if self.customer_id == '0':
            self.customer_id = get_random_string(length=10, allowed_chars='1234567890')

        super(Customer, self).save(*args, **kwargs)
    

    def payments(self):
        if Payment.objects.filter(customer=self).exists():
            return Payment.objects.filter(customer=self)[0]
        return None


isp_choices =  (("ION","ION"),("Alliance Broadband","Alliance Broadband"),("BSNL","BSNL"),("Other","Other"))

class AdditionalData(models.Model):
    plan_type = models.CharField(max_length=255, blank=True, null=True)
    activation_date = models.DateField(null=True, blank=True)
    isp_name = models.CharField(max_length=255, blank=True, null=True,choices=isp_choices)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.customer.user.username
    

class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    install_amount = models.FloatField()
    bill_amount = models.FloatField()
    cable_amount = models.FloatField()
    payment_recieved = models.FloatField()
    balance = models.FloatField()

    def __str__(self):
        return self.customer.user.username
    

    def save(self, *args, **kwargs):
        self.balance = float(self.payment_recieved) - (float(self.bill_amount) + float(self.cable_amount) + float(self.install_amount))
        super(Payment, self).save(*args, **kwargs)



class StaffMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    addhar_number = models.TextField()
    pan_number = models.TextField()
    date_joined = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def get_complaints(self):
        return Complaint.objects.filter(created_by=self.user)
    

class Technician(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    addhar_number = models.TextField()
    pan_number = models.TextField()
    date_joined = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def get_complaints(self):
        return Complaint.objects.filter(assigned_to=self)
    
    def over_due_complaints(self):
        return Complaint.objects.filter(assigned_to=self, created_at__lt=timezone.now()-timedelta(days=2))
    
    def provisioned_requests(self):
        return NewConnectionRequest.objects.filter(assigned_to=self)

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    staff_member = models.ForeignKey(StaffMember, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' ' + str(self.date) + ' ' + str(self.time_in) + ' ' + str(self.time_out)


class NewConnectionRequest(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    status = models.CharField(max_length=255, default='Pending')
    assigned_to = models.ForeignKey(Technician, on_delete=models.CASCADE, blank=True, null=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.name + ' ' + self.phone_number + ' ' + str(self.date)