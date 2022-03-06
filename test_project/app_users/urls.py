from django.urls import path
from .views import AccountView, LogInView, RegisterView, LogOutView, MainPage, FindReceiverView, TransferView


urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('account/', AccountView.as_view(), name='account'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('find_receiver/', FindReceiverView.as_view(), name='find_receiver'),
    path('transfer/', TransferView.as_view(), name='transfer')
]