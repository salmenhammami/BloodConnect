from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/donneur/", views.register_donneur, name="register_donneur"),
    path("register/hopital/", views.register_hopital, name="register_hopital"),
]
