from django.shortcuts import render
from .models import Complaint
from users.models import Technician,Customer,Partner,StaffMember
from django.contrib import messages
from users.decorators import group_required
from django.contrib.auth.decorators import login_required

# Create your views here.

@group_required(("Staff","Admin","Partner"))
@login_required
def home(request):
    user = request.user
    try:
        staff = StaffMember.objects.get(user=user)
        partner = staff.partner
    except:
        pass
    try:
        partner = Partner.objects.get(user=user)
    except:
        pass
    
    active_complaints = Complaint.objects.filter(is_active=True,partner=partner).exclude(status="Resolved",is_resolved=True)
    resolved_complaints = Complaint.objects.filter(is_active=True, status="Resolved",is_resolved=True,partner=partner)
    unique_client_complaints = Customer.objects.filter(partner=partner).count()
   
    technicians = Technician.objects.filter(partner=partner)
    context = {
        "active_complaints": active_complaints,
        "resolved_complaints": resolved_complaints,
        "unique_client_complaints": unique_client_complaints,
        "technicians": technicians
    }
    return render(request, "complaints/complaints_dash.html",context)


@group_required(("Staff","Admin","Partner"))
def create_complaint(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = request.POST.get("priority")
        assigned_to = request.POST.get("assigned_to")
        created_by = request.user
        customer_id = request.POST.get("client_id")
        print(assigned_to)

        customer = Customer.objects.get(id=customer_id)
        partner = customer.partner
        technician = Technician.objects.get(id=assigned_to)

        Complaint.objects.create(
            title=title,
            description=description,
            priority=priority,
            assigned_to=technician,
            created_by=created_by,
            customer=customer,
            partner=partner
        )

        messages.success(request, "Complaint Created Successfully")

    return render(request, "complaints/create_complaint.html")


@group_required(("Staff","Admin","Partner"))
def view_complaint(request, pk):
    complaint = Complaint.objects.get(id=pk)
    context = {
        "complaint": complaint
    }
    return render(request, "complaints/view_complaint.html", context)