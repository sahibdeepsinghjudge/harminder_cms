from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import Partner, Customer, StaffMember, Technician, AdditionalData, Payment, NewConnectionRequest
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from inventory.models import DeviceDetail, AttachedDevice
from .decorators import group_required
from complaints.models import Complaint

from django.db import transaction





def return_user_partner(request):
        user = request.user
        
        try:
            staff = StaffMember.objects.get(user=user)
            partner = staff.partner
            # if user is staff
        except:
            pass

        try:
            # if user is partner and admin is partner also
            partner = Partner.objects.get(user=user)
        except:
            pass
        
        if partner:
            return partner
        return None


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
    partner = return_user_partner(request)
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
        connection_type = request.POST.get("connection_type")
        plan_type = request.POST.get("plan_type")
        activation_date = timezone.now()
        isp_name = request.POST.get("isp_name")

        install_amount = request.POST.get("install_amount") or 0
        bill_amount = request.POST.get("bill_amount") or 0

        payment_recieved = request.POST.get("payment_recieved") or 0

        # cable_length = request.POST.get("cable_length") or 0
        # cable_type = request.POST.get("cable_type")
        # devices_attached = request.POST.getlist("devices_selected")

        # print(devices_attached)
        # devices_attached = devices_attached[0].split(",")

        # if devices_attached[0] != "":
        #     devices_attached = [
        #        data.split("-") for data in devices_attached
        #     ]
        #     # print(devices_attached)
        #     devices_attached = [
        #         {
        #         "id":int(i[0]),
        #         "mac":i[1],
        #         "ip":i[2],
        #         } 
        #     for i in devices_attached
        #     ]
        # else:
        #     devices_attached = []
        
        

        # print(devices_attached)

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Exists")
            return redirect("create_customer")

        password = name[:4] + "@" + phone[-4:]

        user = User.objects.create_user(email=email, username=name.replace(" ", "_"),first_name=name)
        user.set_password(password)
        user.save()

        customer = Customer(user=user, address=address, city=city, state=state, zip_code=zip_code, phone=phone, addhar_number=addhar_number, pan_number=pan_number,partner=partner,connection_type=connection_type)
        customer.save()

        details = AdditionalData.objects.create(plan_type=plan_type, activation_date=activation_date, isp_name=isp_name, customer=customer)
        details.save()

        # price_for_devices = 0
        # for d in devices_attached:
        #     device = DeviceDetail.objects.get(id=d["id"])
        #     attached_device = AttachedDevice.objects.create(device=device, serial_number=d["ip"], mac_address=d["mac"])
        #     customer.devices.add(attached_device)
        #     price_for_devices += device.price_per_unit

        # cable_price = 0
        # cable = DeviceDetail.objects.get(id=cable_type)
        # cable_price = cable.price_per_unit
        # cable_amount = cable_price * int(cable_length)
        payment = Payment.objects.create(customer=customer, install_amount=int(install_amount), bill_amount=bill_amount, cable_amount=0, payment_recieved=payment_recieved,balance=0)
        messages.success(request, "Customer Created Successfully")
        return redirect("configure-devices",customer.customer_id)
    # cables = DeviceDetail.objects.filter(device_type="Cable",added_by = partner.user)
    # deivces = DeviceDetail.objects.filter(added_by = partner.user).exclude(device_type="Cable")

    return render(request, "users/create_customer.html")




def configure_devices(request,cid):
    customer = Customer.objects.get(customer_id=cid)
    isp_devices = DeviceDetail.objects.filter(added_by=customer.partner.user,provider_type="ISP").exclude(device_type="Cable")
    camera_devices = DeviceDetail.objects.filter(added_by=customer.partner.user,provider_type="Camera Connection").exclude(device_type="Cable")
    camera_cables = DeviceDetail.objects.filter(device_type="Cable",added_by = customer.partner.user,provider_type="Camera Connection")
    isp_cables = DeviceDetail.objects.filter(device_type="Cable",added_by = customer.partner.user,provider_type="ISP")
    return render(request, "users/configure_devices.html",{"customer":customer,"isp_devices":isp_devices,"camera_devices":camera_devices, "isp_cables":isp_cables,"camera_cables":camera_cables})


@group_required(("Staff", "Partner","Admin"))
@transaction.atomic
def remove_connected_device(request,cid,did):
    customer = Customer.objects.get(customer_id=cid)
    device = AttachedDevice.objects.get(id=did)
    customer.devices.remove(device)
    customer.save()
    price_for_devices = 0
    devices_attached = customer.devices.all()
    for d in devices_attached:
        device = d.device
        # attached_device = AttachedDevice.objects.create(device=device, serial_number=d["ip"], mac_address=d["mac"])
        # customer.devices.add(attached_device)
        price_for_devices += device.price_per_unit
    pay = Payment.objects.get(customer=customer)
    pay.install_amount = device.price_per_unit
    pay.save()
    return redirect("configure-devices",customer.customer_id)


@group_required(("Staff", "Partner","Admin"))
@transaction.atomic
def add_connected_device(request,cid):
    customer = Customer.objects.get(customer_id=cid)

    if request.method == "POST":
        device_attached = request.POST.get("device")
        device = DeviceDetail.objects.get(id=device_attached)
        device.stock_value = device.stock_value - 1
        device.save()
        mac = request.POST.get("mac")
        ip = request.POST.get("ip")
        attached_device = AttachedDevice.objects.create(device=device, serial_number=ip, mac_address=mac)
        customer.devices.add(attached_device)
        customer.save()
        price_for_devices = 0
        devices_attached = customer.devices.all()
        for d in devices_attached:
            device = d.device
            if device.device_type == "Cable":
                continue
            price_for_devices += device.price_per_unit
        pay = Payment.objects.get(customer=customer)
        pay.install_amount = price_for_devices
        pay.save()
        messages.success(request, "Device Added Successfully")
        return redirect("configure-devices",customer.customer_id)
    else:
        messages.error(request, "Invalid request")
        return redirect("configure-devices",customer.customer_id)
    

@transaction.atomic
@group_required(("Staff", "Partner","Admin"))
def add_update_cable(request,cid):
    customer = Customer.objects.get(customer_id=cid)
    if request.method == "POST":
        cable_length = request.POST.get("cable_length")
        cable_type = request.POST.get("cable_type")
        cable = DeviceDetail.objects.get(id=cable_type)
        ad = AttachedDevice.objects.create(device=cable, serial_number=cable_length, mac_address=cable_length)
        customer.devices.add(ad)
        customer.save()
        cable_price = cable.price_per_unit
        cable_cost = cable_price * int(cable_length)
        pay = Payment.objects.get(customer=customer)
        pay.cable_amount += cable_cost
        pay.save()
        messages.success(request, "Cable Added Successfully")
        return redirect("configure-devices",customer.customer_id)
    else:
        messages.error(request, "Invalid request")
        return redirect("configure-devices",customer.customer_id)



@group_required(("Staff", "Partner","Admin"))
@transaction.atomic
def activate_user_account(request,cid):
    customer = Customer.objects.get(customer_id=cid)
    customer.is_active = True
    customer.save()
    messages.success(request, "User Activated Successfully")
    return redirect("clients")


@group_required(("Staff", "Partner","Admin","Technician"))
@transaction.atomic
def clients(request):
    partner = return_user_partner(request)
    active_clients = Customer.objects.filter(is_active=True,partner=partner)
    inactive_clients = Customer.objects.filter(is_active=False,partner=partner)
    total = active_clients.count() + inactive_clients.count()
    recent_clients = Customer.objects.filter(is_active=True,partner=partner).order_by("-id")[:5]
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
        start_complaint = request.POST.get("start_complaint") == "True"
        user_search = request.POST.get("user_search") == "True"

        customer = Customer.objects.filter(phone=number).first()
        
        if customer:
            if start_complaint:
                technicians = Technician.objects.filter(user__is_active=True, partner=customer.partner.id)
                return render(request, "complaints/create_complaint.html", {"client": customer, "technicians": technicians})
            elif user_search:
                return render(request, "users/customer_details.html", {"users": customer})
        else:
            messages.error(request, "User Not Found. Please create the user first before starting a complaint.")
            return redirect(f"/accounts/provisioning/request/?phone_number={number}&next=True")
        
    return render(request, "users/clients.html")


@transaction.atomic
def new_connection_request(request):
    redirect_url = request.GET.get("next")
    phone_number = request.GET.get("phone_number")


    partner = return_user_partner(request)

    if request.method == "POST":
        name = request.POST.get("name")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        description = request.POST.get("description")
        assigned_to = request.POST.get("assigned_to")
        request_type = request.POST.get("request_type")

        technician = Technician.objects.get(id=assigned_to)
        if NewConnectionRequest.objects.filter(phone_number=phone_number,request_type=request_type).exclude(is_completed=True).exists():
            messages.error(request, "Request Already Exists")
            return redirect("new_connection_request")
        new_connection = NewConnectionRequest.objects.create(name=name, phone_number=phone_number, address=address, description=description, partner=partner, assigned_to=technician, request_type=request_type)

        messages.success(request, "Request Created Successfully")
        return redirect("dashboard")
    
    technicians = Technician.objects.filter(partner=partner)
    return render(request, "users/new_connection_request.html", {"technicians":technicians, "phone_number":phone_number, "redirect_url":redirect_url})
    

@group_required(("Staff", "Partner","Admin","Technician"))
def new_conn_dash(request):
    partner = return_user_partner(request)

    pending_conn = NewConnectionRequest.objects.filter(partner=partner,status="Pending")
    camera_connections = NewConnectionRequest.objects.filter(partner=partner,request_type="Camera Connection")
    new_internet_connections = NewConnectionRequest.objects.filter(partner=partner,request_type="New Internet Connection")
    conersions = NewConnectionRequest.objects.filter(partner=partner,is_completed=True)
    recent_clients = NewConnectionRequest.objects.filter(partner=partner).order_by("-id")
    context={
        "pending_conn":pending_conn,
        "conersions":conersions,
        "recent_clients":recent_clients,
        "new_isp":new_internet_connections,
        "camera_connections":camera_connections
    }
    return render(request, "users/new_connections_dash.html", context)


@group_required(("Staff", "Partner","Admin","Technician"))
def technicians_dash(request):
    partner = return_user_partner(request)
    technicians = Technician.objects.filter(partner=partner)
    complaints = Complaint.objects.filter(assigned_to__in=technicians,partner=partner)
    connections = NewConnectionRequest.objects.filter(assigned_to__in=technicians,partner=partner)
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
    if user.is_superuser:
        partner = None
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


def logout_view(request):
    logout(request)
    return redirect("login")


def client_details(request,pk):
    if request.method == "POST":
        phone = request.POST.get("phone_number")
        address = request.POST.get("address")
        city = request.POST.get("city")
        zip_code = request.POST.get("pincode")
        addhar_number = request.POST.get("addhar_number")   
        pan_number = request.POST.get("pan_number")

        plan_type = request.POST.get("plan_type")
        isp_name = request.POST.get("isp_name")

        install_amount = request.POST.get("install_amount") or 0
        bill_amount = request.POST.get("bill_amount") or 0
        payment_recieved = request.POST.get("payment_recieved") or 0
        cable_length = request.POST.get("cable_length") or 0

        # cable = DeviceDetail.objects.get(id=cable_id)
        # cable_price = cable.price_per_unit
        # cable_cost = cable_price * int(cable_length)

        customer = Customer.objects.get(id=pk)
        customer.zip_code = zip_code
        customer.addhar_number = addhar_number
        customer.pan_number = pan_number
        customer.phone = phone
        customer.address = address
        customer.city = city
        customer.save()

        payment = Payment.objects.get(customer=customer)
        payment.install_amount = install_amount
        payment.bill_amount = bill_amount
        payment.payment_recieved = payment_recieved
        payment.save()
        ad = AdditionalData.objects.get(customer=customer)
        ad.plan_type = plan_type
        ad.isp_name = isp_name
        ad.save()


    client = Customer.objects.get(id=pk)
    devices = DeviceDetail.objects.filter(added_by=client.partner.user).exclude(device_type="Cable")
    cables = DeviceDetail.objects.filter(device_type="Cable",added_by = client.partner.user)

    return render(request,"users/client_details.html",{"client":client,"devices":devices,"cables":cables})