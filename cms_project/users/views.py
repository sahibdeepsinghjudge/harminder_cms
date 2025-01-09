from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import Partner, Customer, StaffMember, Technician, AdditionalData, Payment
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils import timezone
from inventory.models import DeviceDetail, AttachedDevice
from .decorators import group_required


# Create your views here.

def home(request):
    return HttpResponse("Hello, World! from users app")



@group_required("Staff")
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



@group_required(("Staff", "Partner"))
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
        devices_attached = [int(i) for i in devices_attached]


        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Exists")
            return redirect("create_customer")

        password = name[:4] + "@" + phone[-4:]

        user = User.objects.create_user(email=email, username=name.replace(" ", "_"),first_name=name)
        user.set_password(password)
        user.save()

        customer = Customer(user=user, address=address, city=city, state=state, zip_code=zip_code, phone=phone, addhar_number=addhar_number, pan_number=pan_number)
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
