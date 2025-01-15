from django.shortcuts import render
from .models import DeviceDetail
from django.contrib import messages
from users.models import Partner, StaffMember
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from users.decorators import group_required
# Create your views here.

@group_required("Staff","Admin","Partner")
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

    devices = DeviceDetail.objects.filter(added_by=partner.user)
    total_stock_value = sum(device.stock_value() for device in devices)
    total_stock = sum(device.quantity for device in devices)

    paginator = Paginator(devices, 10)  # Show 10 devices per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "total_devices": devices.count(),
        "devices": page_obj,
        "total_stock_value": total_stock_value,
        "total_stock": total_stock
    }
    return render(request, "inventory/inventory_dash.html", context)



@group_required("Staff","Admin","Partner")
def create_device(req):
    user = req.user

    try:
        staff = StaffMember.objects.get(user=user)
        partner = staff.partner
    except:
        pass

    try:
        partner = Partner.objects.get(user=user)
    except:
        pass

    if req.method == "POST":
        name = req.POST.get("name")
        serial_number = req.POST.get("serial_number")
        mac_address = req.POST.get("mac_address")
        quantity = req.POST.get("quantity")
        units = req.POST.get("units")
        price_per_unit = req.POST.get("price_per_unit")
        device_type = req.POST.get("device_type")
        in_stock = req.POST.get("in_stock") == 'on'
        hsn_code = req.POST.get("hsn_code")
        image = req.FILES.get("image")
        description = req.POST.get("description")

        DeviceDetail.objects.create(
            added_by=partner.user,
            name=name,
            serial_number=serial_number,
            mac_address=mac_address,
            quantity=quantity,
            units=units,
            price_per_unit=price_per_unit,
            device_type=device_type,
            in_stock=in_stock,
            hsn_code=hsn_code,
            image=image,
            description=description
        )
        messages.success(req,"Device Created Successfully")

    device_groups = DeviceDetail.objects.filter(added_by=partner.user).values('device_type').annotate(total_quantity=models.Sum('quantity'))
    context = {
        "device_groups": device_groups
    }
    return render(req, "inventory/create_device.html",context= context)



@group_required("Staff","Admin","Partner")
def view_and_update_device(req, id):
    if req.method=="POST":
        device = DeviceDetail.objects.get(id=id)
        device.name = req.POST.get("name")
        device.serial_number = req.POST.get("serial_number")
        device.mac_address = req.POST.get("mac_address")
        device.quantity = req.POST.get("quantity")
        device.units = req.POST.get("units")
        device.price_per_unit = req.POST.get("price_per_unit")
        device.device_type = req.POST.get("device_type")
        device.in_stock = req.POST.get("in_stock") == 'on'
        device.hsn_code = req.POST.get("hsn_code")
        device.image = req.FILES.get("image")
        device.description = req.POST.get("description")
        device.save()
        messages.success("Device Updated Successfully")
        return render(req, "inventory/view_and_update_device.html",{"device":device})
    device = DeviceDetail.objects.get(id=id)
    context = {
        "device": device
    }
    return render(req, "inventory/view_and_update_device.html",context)
