from typing import List
from .utils import send_money
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
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
    """Поиск счёта на который пользователь хочет перевести деньги"""
    def get(self, request):
        return render(self.request, 'app_users/find_receiver.html')

    def post(self, request):
        wallet_id = request.POST['wallet_id']
        wallet = Wallet.objects.select_related('user').only('name', 'user__username').filter(id=wallet_id).first()
        if wallet:
            return render(self.request, 'app_users/find_receiver.html', context={'wallet': wallet})
        else:
            return render(self.request, 'app_users/find_receiver.html', context={'receiver': []})


class TransferView(generic.ListView):
    """Перевод денег другому пользователю"""
    context_object_name = 'wallets'
    template_name = 'app_users/transfer.html'

    def get_queryset(self):
        filtered_user_wallets = Wallet.objects.filter(user_id=self.request.user.id)
        return filtered_user_wallets

    def get_context_data(self, *, object_list=None, **kwargs):
        """Берем из параметров URL ID получателя, чтобы использовать в POST запросе"""
        context = super().get_context_data(**kwargs)
        receiver = self.request.GET.get('receiver_id', '')
        context['receiver_id'] = receiver
        return context

    def post(self, request):
        """Берем ID кошелька, куда совершаем перевод. Затем берем кошельки, выбранные пользователем, с которых
        будем списывать $. Совершаем перевод."""
        wallet_receiver_id: str = request.POST.get('wallet_receiver_id')
        wallets: List[str] = request.POST.getlist('wallet_sender')
        number_money: str = request.POST['number_money']
        try:
            send_money(wallets=wallets, number_money=number_money, wallet_receiver_id=wallet_receiver_id)
            return HttpResponse("Операция проведена успешно.")
        except ValueError as ex:
            return HttpResponse(f"Недостаточно денег на счету №{ex}")



