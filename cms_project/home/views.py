from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models import Partner, Customer, StaffMember, Technician
from users.decorators import group_required

# Create your views here.

@group_required("Staff","Admin","Partner","Technician",login_url="login")
def home(request):
    user = request.user
    if user.is_authenticated == False:
        return redirect("login")
    clients = Customer.objects.filter(is_active=True)
    partners = Partner.objects.all()
    staff = StaffMember.objects.all()
    technicians = Technician.objects.all()
    user_obj = {
        'username': user.username,
        "designation": "Admin" if user.is_superuser else "Staff",
    }
    
    context = {
        "user": user_obj,
        "clients": clients,
        "partners": partners,
        # "staff": staff,
    }   
    return render(request, "home/dashboard.html", context)