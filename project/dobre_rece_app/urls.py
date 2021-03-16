from django.urls import path
from django.contrib import admin
from .views import LandingPage, AddDonation, Login, Register, MyProfile, Logout, \
    Settings, FormConfirmation


urlpatterns = [
    path('', LandingPage.as_view(), name='main'),
    path('add_donation/', AddDonation.as_view(), name='add-donation'),
    path('login/', Login.as_view(), name='login-user'),
    path('register/', Register.as_view(), name='register'),
    path('profile/', MyProfile.as_view(), name='my-profile'),
    path('settings/', Settings.as_view(), name='settings'),
    path('logout/', Logout.as_view(), name='logout-user'),
    path('form_confirmation/', FormConfirmation.as_view(), name='form-confirmation'),
]
