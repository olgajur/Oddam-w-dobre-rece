from django.shortcuts import render, redirect
from django.db.models import Sum
from django.views import View
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserManager, User, Institution, Donation, Category


class LandingPage(View):
    def get(self, request):
        sacks = Donation.objects.all().aggregate(Sum('quantity'))
        institutions = Donation.objects.all().distinct('institution').count()
        if sacks['quantity__sum'] is None:
            sacks = 0
        else:
            sacks = sacks['quantity__sum']
        charities = Institution.objects.filter(type='charity')
        ngos = Institution.objects.filter(type='ngo')
        locals = Institution.objects.filter(type='local')
        ctx = {
            'sacks' : sacks,
            'institutions' : institutions,
            'charities' : charities,
            'ngos' : ngos,
            'locals' : locals
        }
        return render(request, 'index.html', ctx)

class AddDonation(View):
    def get(self, request):
        if request.user.is_authenticated:
            categories = Category.objects.all()
            institutions = Institution.objects.all()
            ctx = {
            'categories' : categories,
            'institutions' : institutions
            }
            return render(request, 'form.html', ctx)
        else:
            return redirect('login-user')

    def post(self, request):
        categories = request.POST.get('categoriesValues')
        categories = categories.split(',')
        sacks = request.POST.get('sacks')
        institution_id = request.POST.get('selectedInstitution')
        institution = Institution.objects.get(pk=institution_id)
        address = request.POST.get('address')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        more_info = request.POST.get('moreInfo')
        new_donation = Donation.objects.create(
        quantity=sacks, institution=institution,
        address=address, phone_number=phone, city=city, zip_code=postcode,
        pick_up_date=date, pick_up_time=time, pick_up_comment=more_info
        )
        # for category in categories:
        new_donation.categories.add(*categories)
        new_donation.save()
        return redirect('form-confirmation')

class Login(View):
    def get(self, request):
        msg = ''
        return render(request, 'login.html', {'msg' : msg})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('/')
        else:
            return redirect('register')

class Register(View):
    def get(self, request):
        return render(request, 'register.html', {})

    def post(self, request):
        user = User()
        email = request.POST.get('email')
        first = request.POST.get('name')
        last = request.POST.get('surname')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if email and first and last and password and password2:
            if password == password2:
                # user.email = email
                # user.first_name = first
                # user.last_name = last
                # user.password = password
                new_user = get_user_model().objects.create_user(
                    email=email,
                    first_name=first,
                    last_name=last,
                    password=password
                )
                new_user.save()
            else:
                raise ValidationError('Podane hasła się różnią.')
        else:
            raise ValidationError('Uzupełnij wszystkie pola')
        return redirect('login-user')

class MyProfile(LoginRequiredMixin, View):
    def get(self, request):
        current_user = self.request.user
        my_donations = Donation.objects.filter(user_id=current_user.pk)
        ctx = {
        'current_user' : current_user,
        'my_donations' : my_donations
        }
        return render(request, 'user-view.html', ctx)

class Settings(View):
    def get(self, request):
        pass

class Logout(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            logout(request)
        return redirect('/')

class FormConfirmation(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'form-confirmation.html', {})
