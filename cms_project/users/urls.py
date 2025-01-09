from django.urls import path
from .views import home, create_partner, login_view,create_customer,search_user,clients

urlpatterns = [
    path("", home, name="home"),
    path("create-partner/", create_partner, name="create_partner"),
    path("login/", login_view, name="login"),
    path("create-customer/", create_customer, name="create-customer"),
    path("clients", clients, name="clients"),
    path('search_user',search_user,name='search_user')
]