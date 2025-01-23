from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models import Partner, Customer, StaffMember, Technician
from users.decorators import group_required
from complaints.models import Complaint

from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required
@group_required(("Staff","Admin","Partner"))
def home(request):
    user = request.user
    if user.is_authenticated == False:
        return redirect("login")
    partner = Partner.objects.filter(user=user).first()
    clients = Customer.objects.filter(is_active=True,partner=partner)
    partners = Partner.objects.all()
    staff = StaffMember.objects.filter(partner=partner)
    technicians = Technician.objects.filter(partner=partner)
    complaints = Complaint.objects.filter(partner=partner)  
    user_obj = {
        'username': user.username,
        "designation": "Admin" if user.is_superuser else "Staff",
    }
    
    context = {
        "user": user_obj,
        "clients": clients,
        "partners": partners,
        "complaints": complaints,
        # "staff": staff,
    }   
    return render(request, "home/dashboard.html", context)