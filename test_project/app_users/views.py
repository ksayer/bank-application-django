from typing import List

from django.contrib.auth import authenticate, login
from django.contrib.auth import views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from .models import Wallet, Transaction, Transfer
from .forms import WalletForm
from .utils import send_money


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
        """Поиск введенного кошелька. Если кошелек найден, то проверяем не принадлежит ли он искателю."""
        wallet_id = request.POST['wallet_id']
        wallet = Wallet.objects.select_related('user').only('name', 'user__username').filter(id=wallet_id).first()
        if wallet:
            if wallet.user_id == request.user.id:
                return render(self.request, 'app_users/find_receiver.html', context={'answer': 'Это ваш счёт'})
            else:
                return render(self.request, 'app_users/find_receiver.html', context={'wallet': wallet})
        else:
            return render(self.request, 'app_users/find_receiver.html', context={'answer': []})


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
        """Берем ID кошелька, куда совершаем перевод. Затем берем кошельки, выбранные пользователем, с которых будем
        списывать $. Совершаем перевод. Если денег не хватило на каком либо счете - сообщаем пользователю и отменяем
        транзакцию """
        wallet_receiver_id: str = request.POST.get('wallet_receiver_id')
        wallets: List[str] = request.POST.getlist('wallet_sender')
        number_money: str = request.POST['number_money']
        try:
            send_money(wallets=wallets, number_money=number_money, wallet_receiver_id=wallet_receiver_id)
            return HttpResponse("Операция проведена успешно.")
        except ValueError as ex:
            return HttpResponse(f"Недостаточно денег на счету №{ex}")


class HistoryView(generic.ListView):
    model = Transaction
    template_name = 'app_users/history.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        """Отбираем транзакции пользователя, только те, в которых он переводил $"""
        user_transactions_as_sender = Transaction.objects.filter(sender_id=self.request.user.id).order_by('-id')
        return user_transactions_as_sender


class WalletDetail(generic.DetailView):
    model = Wallet
    template_name = 'app_users/wallet_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        transfers = Transfer.objects.filter(wallet_id=pk).order_by('-id')
        context['transfers'] = transfers
        return context


class CreateWalletFormView(generic.View):
    def get(self, request):
        form = WalletForm()
        return render(request, 'app_users/create_wallet.html', context={'form': form})

    def post(self, request):
        form = WalletForm(request.POST)
        if form.is_valid():
            form.cleaned_data['user'] = User.objects.get(id=request.user.id)
            Wallet.objects.create(**form.cleaned_data)
            return HttpResponseRedirect(reverse('account'))