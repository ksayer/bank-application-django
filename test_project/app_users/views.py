from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import views
from .models import Wallet


class MainPage(generic.TemplateView):
    template_name = 'app_users/main.html'


class AccountView(generic.TemplateView):
    template_name = 'app_users/account.html'


class RegisterView(generic.View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'app_users/registration.html', context={'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/app_users/')
        else:
            return render(request, 'app_users/registration.html', context={'form': form})


class LogInView(views.LoginView):
    template_name = 'app_users/login.html'


class LogOutView(views.LogoutView):
    pass


class FindReceiverView(generic.View):
    def get(self, request):
        return render(self.request, 'app_users/find_receiver.html')

    def post(self, request):
        wallet_id = request.POST['wallet_id']
        wallet = Wallet.objects.select_related('user').only('name', 'user__username').filter(id=wallet_id).first()
        if wallet:
            return render(self.request, 'app_users/find_receiver.html', context={'wallet': wallet})
        else:
            return render(self.request, 'app_users/find_receiver.html', context={'receiver': []})
