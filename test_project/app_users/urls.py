from django.urls import path

from .views import AccountView, LogInView, RegisterView, LogOutView, MainPage, FindReceiverView, TransferView, \
    HistoryView, WalletDetail, CreateWalletFormView, CancelTransaction

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('account/', AccountView.as_view(), name='account'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('find_receiver/', FindReceiverView.as_view(), name='find_receiver'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('account/history/', HistoryView.as_view(), name='history'),
    path('account/history/<int:pk>/', WalletDetail.as_view(), name='wallet_detail'),
    path('app_users/create_wallet/', CreateWalletFormView.as_view(), name='create_wallet'),
    path('app_users/cancel_transaction/', CancelTransaction.as_view(), name='cancel_transaction')
]
