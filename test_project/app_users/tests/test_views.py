from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


USERNAME = 'user'
PASSWORD = 'qweQAZ!@#'


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
        self.assertContains(response, 'Вы не аутентифицированы')
        self.assertContains(response, 'Войти')

    def test_main_page_for_authenticated_user(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse('main'))
        self.assertContains(response, 'Здравствуйте')


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
