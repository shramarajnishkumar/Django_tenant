from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView
from sharedapp.models import User
from authapp.models import Company, Domain
from django.db import transaction
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from sesame.utils import get_query_string, get_token
from datetime import timedelta, datetime


@method_decorator(login_required(login_url='login/'), name='dispatch')
class HomeView(View):
    def get(self, request):
        return render(request, 'sharedapp/home.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'sharedapp/register.html')

    @transaction.atomic
    def post(self, request):
        if request.POST['password'] == request.POST['password2']:
            try:
                company = Company.objects.create(
                    schema_name=request.POST['company_name'],
                    name=request.POST['company_name'],
                    trial_end = datetime.now() + timedelta(days=7)
                )
                user = User.objects.create(
                    username=request.POST['username'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['email'],
                    company=company
                )
                user.set_password(request.POST['password'])
                user.save()

                company_name = company.schema_name
                host = request.get_host().strip(':7000')
                domain = company_name+"."+host
                Domain.objects.create(
                    domain=domain,
                    tenant=company
                )

                scheme_url = request.is_secure() and "https" or "http"
                url = f"{scheme_url}://{domain}:7000/login"

                return redirect(url)
            except Exception as e:
                messages.error(request, e)
                return render(request, 'sharedapp/register.html')
        messages.error(request, 'password and confirm password not match!!')
        return render(request, 'sharedapp/register.html')


class LogInView(View):
    def get(self, request):
        return render(request, 'sharedapp/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            company_name = user.company.schema_name
            scheme_url = request.is_secure() and "https" or "http"
            login_url = f"{scheme_url}://{company_name}.localhost:7000"
            url = login_url + get_query_string(user)
            token = get_token(user)
            user = authenticate(sesame=token)
            return HttpResponseRedirect(url)
        messages.error(request, 'Invalid username or password!!')
        return render(request, 'sharedapp/login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Logged out successfully!")
        return redirect("login")