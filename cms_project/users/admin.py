from django.contrib import admin
from .models import Partner, StaffMember, Technician, Attendance, Customer, Payment, AdditionalData
# Register your models here.


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city', 'state', 'zip_code', 'area', 'phone', 'addhar_number', 'pan_number') 
    search_fields = ('user', 'address', 'city', 'state', 'zip_code', 'area', 'phone', 'addhar_number', 'pan_number')
    list_filter = ('user', 'address', 'city', 'state', 'zip_code', 'area', 'phone', 'addhar_number', 'pan_number')
    list_per_page = 10

admin.site.register(Partner, PartnerAdmin)    

class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city', 'state', 'zip_code', 'phone', 'addhar_number', 'pan_number', 'date_joined', 'date_created', 'partner') 
    search_fields = ('user', 'address', 'city', 'state', 'zip_code', 'phone', 'addhar_number', 'pan_number', 'date_joined', 'date_created', 'partner')
    list_filter = ('user', 'address', 'city', 'state', 'zip_code', 'phone', 'addhar_number', 'pan_number', 'date_joined', 'date_created', 'partner')
    list_per_page = 10

admin.site.register(StaffMember, StaffMemberAdmin)

class TechnicianAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city', 'state', 'zip_code', 'phone', 'addhar_number', 'pan_number', 'date_joined', 'date_created', 'partner') 
    search_fields = ('user', 'address', 'city', 'state', 'zip_code', 'phone', 'addhar_number', 'pan_number', 'date_joined', 'date_created', 'partner')
    list_filter = ('user', 'address', 'city', 'state', 'zip_code', 'phone', 'addhar_number', 'pan_number', 'date_joined', 'date_created', 'partner')
    list_per_page = 10

admin.site.register(Technician, TechnicianAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date') 
    search_fields = ('user', 'date')
    list_filter = ('user', 'date')
    list_per_page = 10

admin.site.register(Attendance, AttendanceAdmin)


admin.site.register(Customer)
admin.site.register(Payment)
admin.site.register(AdditionalData)


