from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import views


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
