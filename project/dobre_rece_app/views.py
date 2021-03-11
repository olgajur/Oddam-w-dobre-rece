from django.shortcuts import render
from django.db.models import Sum
from django.views import View
from .models import Institution, Donation


class LandingPage(View):
    def get(self, request):
        sacks = Donation.objects.all().aggregate(Sum('quantity'))
        institutions = Institution.objects.filter(donation__isnull=False).count()
        if sacks['quantity__sum'] is None:
            sacks = 0
        else:
            sacks = sacks['quantity__sum']
        return render(request, 'index.html', {'sacks' : sacks, 'institutions' : institutions})

class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html', {})

class Login(View):
    def get(self, request):
        return render(request, 'login.html', {})

class Register(View):
    def get(self, request):
        return render(request, 'register.html', {})
