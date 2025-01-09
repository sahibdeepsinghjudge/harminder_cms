from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Complaint(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.IntegerField(max_length=255)
    assigned_to = models.ForeignKey('users.Technician', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, default="Pending")
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolved_description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey('users.Customer', on_delete=models.CASCADE)
    partner = models.ForeignKey('users.Partner', on_delete=models.CASCADE)
    is_resolved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.title} -- {self.customer}"
