from django.contrib import admin
from .models import Wallet, Transaction, Transfer


class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'balance', 'name']
    list_filter = ['user']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'receiver', 'sender']
    list_filter = ['date', 'receiver', 'sender']


class TransferAdmin(admin.ModelAdmin):
    list_display = ['id', 'wallet', 'operation', 'date']
    list_filter = ['wallet', 'date']


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Transfer, TransferAdmin)





