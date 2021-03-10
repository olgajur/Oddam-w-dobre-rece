from django.urls import path
from django.contrib import admin
from .views import LandingPage, AddDonation, Login, Register

urlpatterns = [
    path('', LandingPage.as_view(), name='main'),
    path('add_item/', AddDonation.as_view(), name='add-donation'),
    path('login/', Login.as_view(), name='login-user'),
    path('register/', Register.as_view(), name='register'),
]
