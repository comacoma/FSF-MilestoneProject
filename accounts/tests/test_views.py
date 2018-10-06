from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

"""
This project uses default user model provided by django without any extension
or modification, hence it is not needed to test the model itself. However
it is necessary to test the authentication behaviour (i.e. login/ logout/
registration)
"""

class TestLoginView(TestCase):
    def test_view_status(self):
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    # def test_page_contains_correct_html(self):
    #     response = self.client.get('/acounts/login/')
    #     self.assertContains(response, '<p>Login using your username or email</p>')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/accounts/login/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

"""
Referring code from https://stackoverflow.com/questions/22457557/how-to-test-login-process
"""
class TestLoginBehaviour(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post('/accounts/login/', {'username': 'testuser', 'password': 'secret'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
