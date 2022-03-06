from django.contrib.auth.models import User
from django.db import models


class Wallet(models.Model):
    """Модель счёта пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets', verbose_name='Пользователь')
    balance = models.PositiveIntegerField(default=0, verbose_name='Баланс')
    name = models.CharField(max_length=128, verbose_name='Название')

    def __str__(self):
        return f"{self.name}({self.user})"

    class Meta:
        verbose_name = 'счёт'
        verbose_name_plural = 'счета'


class Transaction(models.Model):
    """Модель транзакции"""
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_receiver', verbose_name='Получатель')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_sender', verbose_name='Отправитель')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return f"ID{self.id}.{self.date}: {self.sender} -> {self.receiver}"

    class Meta:
        verbose_name = 'транзакция'
        verbose_name_plural = 'транзакции'


class Transfer(models.Model):
    """Модель произведения операции с кошельком (изменения баланса)"""
    OPERATION_CHOICES = [
        ('r', 'Пополнение'),
        ('s', 'Снятие')
    ]
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE,
                                    related_name='transfers', verbose_name='Транзакция')
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transfers', verbose_name='Счёт')
    number = models.PositiveIntegerField(default=0, verbose_name='Количество')
    operation = models.CharField(max_length=1, choices=OPERATION_CHOICES, verbose_name='Операция')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return f"{self.id}.{self.wallet}"

    class Meta:
        verbose_name = 'перевод'
        verbose_name_plural = 'переводы'


