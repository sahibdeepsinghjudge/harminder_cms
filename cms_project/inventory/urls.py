from django.urls import path

from .views import home,create_device

urlpatterns = [
    path("", home, name="inventory_dash"),
    path("create-device/", create_device, name="create-device"),
]