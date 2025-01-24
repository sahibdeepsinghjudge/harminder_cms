from django.urls import path
from .views import home, create_partner, login_view,create_customer,search_user,clients,new_connection_request,new_conn_dash,technicians_dash,create_technician,logout_view, client_details,configure_devices, remove_connected_device, add_connected_device, activate_user_account, add_update_cable 

urlpatterns = [
    path("", home, name="home"),
    path("create-partner/", create_partner, name="create_partner"),
    path("login/", login_view, name="login"),
    path("create-customer/", create_customer, name="create-customer"),
    path("clients", clients, name="clients"),
    path('search_user',search_user,name='search_user'),
    path('provisioning/request/',new_connection_request,name='create-connection-request'),
    path('provisioning/dashboard',new_conn_dash,name='new-conn-dash'),
    path('technicians/dashboard',technicians_dash,name='tech-dash'),
    path('create-technician/',create_technician,name='create-technician'),
    path('logout/',logout_view,name='logout'),
    path('client-details/<int:pk>/',client_details,name='client-details'),
    path('configure-devices/<str:cid>',configure_devices,name='configure-devices'),
    path('remove-connected-device/<str:cid>/<str:did>',remove_connected_device,name='remove-connected-device'),
    path('add-connected-device/<str:cid>',add_connected_device,name='add-connected-device'),
    path('activate-account/<str:cid>',activate_user_account,name='activate-account'),
    path('add-update-cable/<str:cid>',add_update_cable,name='add-update-cable')
]