from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from ..models import Wallet, Transaction

USERNAME = 'user'
USERNAME_2 = 'user2'
PASSWORD = 'qweQAZ!@#'
NAME = 'name'
BALANCE = 1000
SEND_MONEY = 300


class MainPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username=USERNAME,
            password=PASSWORD
        )

    def test_main_page_url_exists(self):
        response = self.client.get('/app_users/')
        self.assertEqual(response.status_code, 200)

    def test_main_page_uses_right_template(self):
        response = self.client.get(reverse('main'))
        self.assertTemplateUsed(response, 'app_users/main.html')

    def test_main_page_for_not_authenticated_user(self):
        response = self.client.get(reverse('main'))
        self.assertContains(response, 'Зарегистрироваться')

    def test_main_page_for_authenticated_user(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse('main'))
        self.assertContains(response, 'Выйти')


class TestAccountPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username=USERNAME,
            password=PASSWORD
        )

    def test_account_url_exists(self):
        response = self.client.get('/app_users/account/')
        self.assertEqual(response.status_code, 200)

    def test_account_uses_right_template(self):
        response = self.client.get(reverse('account'))
        self.assertTemplateUsed(response, 'app_users/account.html')

    def test_page_for_not_authenticated_user(self):
        response = self.client.get(reverse('account'))
        self.assertContains(response, 'Вы не аутентифицированы')
        self.assertContains(response, 'Войти')

    def test_page_for_authenticated_user(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse('account'))
        self.assertContains(response, 'Добро пожаловать')


class TestRegister(TestCase):

    def test_register_page_url_exists(self):
        response = self.client.get('/app_users/registration/')
        self.assertEqual(response.status_code, 200)

    def test_register_page_uses_right_template(self):
        response = self.client.get(reverse('registration'))
        self.assertTemplateUsed(response, 'app_users/registration.html')

    def test_register_post(self):
        response = self.client.post(reverse('registration'), data={'username': USERNAME,
                                                                   'password1': PASSWORD,
                                                                   'password2': PASSWORD})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/app_users/')


class TestLoginLogout(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username=USERNAME,
            password=PASSWORD
        )

    def test_login_page_url_exists(self):
        response = self.client.get('/app_users/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_uses_right_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'app_users/login.html')
        self.assertContains(response, 'Войти')

    def test_login_post(self):
        response = self.client.post(reverse('login'), data={'username': USERNAME,
                                                            'password': PASSWORD})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/app_users/')

    def test_logout(self):
        response = self.client.get('/app_users/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/app_users/')


class TestFindReceiver(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username=USERNAME,
            password=PASSWORD
        )
        Wallet.objects.create(
            user=user,
            name=NAME
        )

    def test_find_receiver_page_uses_right_url(self):
        response = self.client.get('/app_users/find_receiver/')
        self.assertEqual(response.status_code, 200)

    def test_find_receiver_uses_right_template(self):
        response = self.client.get(reverse('find_receiver'))
        self.assertTemplateUsed(response, 'app_users/find_receiver.html')

    def test_post(self):
        response = self.client.post((reverse('find_receiver')), data={'wallet_id': 1})
        self.assertEqual(response.status_code, 200)


class TestTransferMoney(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username=USERNAME,
            password=PASSWORD
        )
        user_2 = User.objects.create_user(
            username=USERNAME_2,
            password=PASSWORD
        )
        Wallet.objects.create(
            user=user,
            name=NAME,
            balance=BALANCE
        )

        Wallet.objects.create(
            user=user,
            name=NAME,
            balance=BALANCE
        )

        Wallet.objects.create(
            user=user_2,
            name=NAME,
            balance=BALANCE
        )

    def test_transfer_page_uses_right_url(self):
        response = self.client.get('/app_users/transfer/')
        self.assertEqual(response.status_code, 200)

    def test_transfer_uses_right_template(self):
        response = self.client.get(reverse('transfer'))
        self.assertTemplateUsed(response, 'app_users/transfer.html')

    def test_post_enough_money(self):
        self.client.post(reverse('transfer'), data={'wallet_sender': [1, 2],
                                                    'wallet_receiver_id': 3,
                                                    'number_money': SEND_MONEY})
        check_money_sender = Wallet.objects.get(id=1).balance
        check_money_receiver = Wallet.objects.get(id=3).balance
        self.assertEqual(check_money_sender, BALANCE - (SEND_MONEY / 2))
        self.assertEqual(check_money_receiver, BALANCE + SEND_MONEY)

    def test_post_not_enough_money(self):
        self.client.post(reverse('transfer'), data={'wallet_sender': [1, 2],
                                                    'wallet_receiver_id': 3,
                                                    'number_money': SEND_MONEY * 10})
        check_money_sender = Wallet.objects.get(id=1).balance
        check_money_receiver = Wallet.objects.get(id=3).balance
        self.assertEqual(check_money_sender, BALANCE)
        self.assertEqual(check_money_receiver, BALANCE)


class TestHistoryTransaction(TestCase):

    def test_history_page_uses_right_url(self):
        response = self.client.get('/app_users/account/history/')
        self.assertEqual(response.status_code, 200)

    def test_history_page_uses_right_template(self):
        response = self.client.get(reverse('history'))
        self.assertTemplateUsed(response, 'app_users/history.html')
