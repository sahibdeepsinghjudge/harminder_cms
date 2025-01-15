from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import Partner, Customer, StaffMember, Technician, AdditionalData, Payment, NewConnectionRequest
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils import timezone
from inventory.models import DeviceDetail, AttachedDevice
from .decorators import group_required
from complaints.models import Complaint

from django.db import transaction


# Create your views here.

def home(request):
    return HttpResponse("Hello, World! from users app")


@group_required("Staff","Admin")
@transaction.atomic
def create_partner(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")
        area = request.POST.get("area")
        phone = request.POST.get("phone")
        addhar_number = request.POST.get("addhar_number")
        pan_number = request.POST.get("pan_number")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Exists")
            return redirect("create_partner")
        if Partner.objects.filter(phone=phone,pan_number=pan_number,addhar_number=addhar_number).exists():
            messages.error(request, "Detalis Already Exists")
            return redirect("create_partner")
        
        user = User.objects.create_user(email=email, username=name.replace(" ", "_"))
        password = name[:4] + "@" + phone[-4:]
        print(password)
        user.set_password(password)
        user.save()

        partner = Partner(user=user, address=address, city=city, state=state, zip_code=zip_code, area=area, phone=phone, addhar_number=addhar_number, pan_number=pan_number)
        partner.save()
        messages.success(request, "Partner Created Successfully")
        return redirect("dashboard")
    
    return render(request, "users/create_partner.html")




def login_view(request):
    if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login Successfull")
                request.session["user"] = user.username
                if user.is_superuser:
                    request.session["status"] = "Admin"
                elif user.is_staff:
                    request.session["status"] = "Staff"
                else:
                    request.session["status"] = "Partner"
                return redirect("dashboard")
    return render(request, "users/login.html")



@group_required(("Staff", "Partner","Admin"))
@transaction.atomic
def create_customer(request):
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
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone_number")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("pincode")
        addhar_number = request.POST.get("addhar_number")   
        pan_number = request.POST.get("pan_number")

        plan_type = request.POST.get("plan_type")
        activation_date = timezone.now()
        isp_name = request.POST.get("isp_name")

        install_amount = request.POST.get("install_amount") or 0
        bill_amount = request.POST.get("bill_amount") or 0
        cable_length = request.POST.get("cable_length") or 0
        cable_type = request.POST.get("cable_type")
        payment_recieved = request.POST.get("payment_recieved") or 0
        devices_attached = request.POST.getlist("devices_selected")
        print(devices_attached)
        if devices_attached[0] != "":
            devices_attached = [int(i) for i in devices_attached]
        else:
            devices_attached = []


        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Exists")
            return redirect("create_customer")

        password = name[:4] + "@" + phone[-4:]

        user = User.objects.create_user(email=email, username=name.replace(" ", "_"),first_name=name)
        user.set_password(password)
        user.save()

        customer = Customer(user=user, address=address, city=city, state=state, zip_code=zip_code, phone=phone, addhar_number=addhar_number, pan_number=pan_number,partner=partner)
        customer.save()

        details = AdditionalData.objects.create(plan_type=plan_type, activation_date=activation_date, isp_name=isp_name, customer=customer)
        details.save()

        price_for_devices = 0
        for device in devices_attached:
            device = DeviceDetail.objects.get(id=device)
            attached_device = AttachedDevice.objects.create(device=device, serial_number=0000, mac_address=000)
            customer.devices.add(attached_device)
            price_for_devices += device.price_per_unit

        cable_price = 0
        cable = DeviceDetail.objects.get(id=cable_type)
        cable_price = cable.price_per_unit
        cable_amount = cable_price * int(cable_length)
        payment = Payment.objects.create(customer=customer, install_amount=int(install_amount)+price_for_devices, bill_amount=bill_amount, cable_amount=cable_amount, payment_recieved=payment_recieved,balance=0)

        messages.success(request, "Customer Created Successfully")
        return redirect("dashboard")
    cables = DeviceDetail.objects.filter(device_type="Cable",added_by = partner.user)
    deivces = DeviceDetail.objects.filter(added_by = partner.user).exclude(device_type="Cable")

    return render(request, "users/create_customer.html", {"cables":cables,"devices":deivces})


@group_required(("Staff", "Partner","Admin","Technician"))
@transaction.atomic
def clients(request):
    active_clients = Customer.objects.filter(is_active=True)
    inactive_clients = Customer.objects.filter(is_active=False)
    total = active_clients.count() + inactive_clients.count()
    recent_clients = Customer.objects.filter(is_active=True).order_by("-id")[:5]
    context={
        "active_clients":active_clients,
        "inactive_clients":inactive_clients,
        "total":total,
        "recent_clients":recent_clients
    }
    return render(request, "users/clients.html", context)


def search_user(request):
    if request.method == "POST":
        number = request.POST.get("number")
        start_complaint = request.POST.get("start_complaint")
        user_search = request.POST.get("user_search")
        customer = Customer.objects.filter(phone=number)
        customer = customer[0] if customer else None
        if customer:
            if start_complaint == "True":
                technicians = Technician.objects.filter(user__is_active=True,partner = customer.partner.id)
                return render(request, "complaints/create_complaint.html", {"client":customer,"technicians":technicians})
            elif user_search == "True":
                return render(request, "users/customer_details.html", {"users":customer})
        else:
            messages.error(request, "User Not Found")
        return render(request, "users/clients.html", {"users":customer})
    return render(request, "users/clients.html")


@transaction.atomic
def new_connection_request(request):
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

    if request.method == "POST":
        name = request.POST.get("name")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        description = request.POST.get("description")
        assigned_to = request.POST.get("assigned_to")

        technician = Technician.objects.get(id=assigned_to)
        if NewConnectionRequest.objects.filter(phone_number=phone_number).exclude(is_completed=True).exists():
            messages.error(request, "Request Already Exists")
            return redirect("new_connection_request")
        new_connection = NewConnectionRequest.objects.create(name=name, phone_number=phone_number, address=address, description=description, partner=partner, assigned_to=technician)

        messages.success(request, "Request Created Successfully")
        return redirect("dashboard")
    
    technicians = Technician.objects.filter(partner=partner)
    return render(request, "users/new_connection_request.html", {"technicians":technicians})
    

@group_required(("Staff", "Partner","Admin","Technician"))
def new_conn_dash(request):
    pending_conn = NewConnectionRequest.objects.filter(status="Pending")
    conersions = NewConnectionRequest.objects.filter(is_completed=True)
    recent_clients = NewConnectionRequest.objects.all().order_by("-id")[:5]
    context={
        "pending_conn":pending_conn,
        "conersions":conersions,
        "recent_clients":recent_clients
    }
    return render(request, "users/new_connections_dash.html", context)


@group_required(("Staff", "Partner","Admin","Technician"))
def technicians_dash(request):
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
    technicians = Technician.objects.filter(partner=partner)
    complaints = Complaint.objects.filter(assigned_to__in=technicians)
    connections = NewConnectionRequest.objects.filter(assigned_to__in=technicians)
    context={
        "technicians":technicians,
        "complaints":complaints,
        "connections":connections
    }
    return render(request, "users/technicians_dash.html", context)


@group_required(("Staff", "Partner","Admin"))
@transaction.atomic
def create_technician(request):
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
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        phone = request.POST.get("phone_number")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")
        addhar_number = request.POST.get("addhar_number")
        pan_number = request.POST.get("pan_number")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Exists")
            return redirect("create-technician")
        
        if Technician.objects.filter(phone=phone,pan_number=pan_number,addhar_number=addhar_number).exists():
            messages.error(request, "Detalis Already Exists")
            return redirect("create-technician")
        
        user = User.objects.create_user(email=email, username=name.replace(" ", "_"))
        password = name[:4] + "@" + phone[-4:]
        print(password)
        user.set_password(password)
        user.save()

        technician = Technician(user=user, address=address, city=city, state=state, zip_code=zip_code, phone=phone, addhar_number=addhar_number, pan_number=pan_number,partner=partner)
        technician.save()
        messages.success(request, "Technician Created Successfully")
        return redirect("dashboard")
    
    return render(request, "users/create_technician.html")