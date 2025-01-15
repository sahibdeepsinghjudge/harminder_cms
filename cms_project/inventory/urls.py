from django.urls import path

from .views import home,create_device,view_and_update_device

urlpatterns = [
    path("", home, name="inventory_dash"),
    path("create-device/", create_device, name="create-device"),
    path("view-update-device/<int:id>/", view_and_update_device, name="view-update-device"),
]