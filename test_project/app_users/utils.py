from typing import List

from django.contrib.auth.models import User
from django.db import transaction

from .models import Wallet, Transaction, Transfer


def reduce_money(wallets: List[str], number_money: str, transact: Transaction):
    """Проходим по всех кошелькам с которых будем списывать денги. Если сумма списания больше баланса -
    вызывается исключение. Создаем на каждый перевод объект трансфера в БД"""
    part_money = int(number_money) / len(wallets)
    wallets = Wallet.objects.filter(id__in=wallets).only('balance')

    for wallet in wallets:
        if wallet.balance < part_money:
            raise ValueError(wallet.id)
        else:
            wallet.balance -= part_money
            wallet.save(update_fields=['balance'])
        Transfer.objects.create(
            operation='s',
            transaction=transact,
            wallet=wallet,
        )


def increase_money(wallet_receiver_id: str, number_money: str, transact: Transaction):
    """Увеличиваем баланс счета получателя. Создаем объект трансфера в БД"""
    wallet = Wallet.objects.only('balance').get(id=wallet_receiver_id)
    wallet.balance += int(number_money)
    wallet.save(update_fields=['balance'])
    Transfer.objects.create(
        operation='r',
        transaction=transact,
        number_money=number_money,
        wallet=wallet,
    )


@transaction.atomic
def send_money(wallets: List[str], number_money: str, wallet_receiver_id: str):
    """Создаем транзакцию. Уменьшаем баланс и если денег хватает, то переводим их на счёт другого пользователя."""
    receiver = User.objects.get(wallets=wallet_receiver_id)
    sender = User.objects.get(wallets=wallets[0])
    transact = Transaction.objects.create(
        receiver=receiver,
        sender=sender,
        number_money=number_money,
    )

    reduce_money(wallets, number_money, transact)
    increase_money(wallet_receiver_id=wallet_receiver_id, number_money=number_money, transact=transact)
