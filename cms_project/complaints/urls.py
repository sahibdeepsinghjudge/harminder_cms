from django.urls import path


from .views import home,create_complaint

urlpatterns = [
    path("", home, name="complaints_dash"),
    path("create-complaint/", create_complaint, name="create-complaint"),
]