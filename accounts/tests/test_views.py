from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User

"""
This project uses default user model provided by django without any extension
or modification, hence it is not needed to test the model itself. However
it is necessary to test the authentication behaviour (i.e. login/ logout/
registration)

Also there is no need to test views related to password change/ reset. This is because
this project uses default views provided by Django for said features, albeit a
custom template is being used.
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

    def test_page_contains_correct_html(self):
        response = self.client.get('/accounts/login/')
        self.assertContains(response, '<p>Login using your username or email</p>')

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
            'email': 'testuser@user.com',
            'password': 'secret'
        }
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post('/accounts/login/', {'username': 'testuser', 'password': 'secret'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_redirect(self):
        response = self.client.post('/accounts/login/', {'username': 'testuser', 'password': 'secret'}, follow=True)
        self.assertRedirects(response, reverse('index'))

    def test_login_message(self):
        response = self.client.post('/accounts/login/', {'username': 'testuser', 'password': 'secret'}, follow=True)
        self.assertContains(response, 'You have successfully logged in!')

    def test_email_login(self):
        response = self.client.post('/accounts/login/', {'username': 'testuser@user.com', 'password': 'secret'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_invalid_login(self):
        response = self.client.post('/accounts/login/', {'username': 'noneuser', 'password': 'secret'}, follow=True) # non-existing user
        self.assertFalse(response.context['user'].is_authenticated)

    """
    This test checks that user will not be directed to login page when logged in already
    """
    def test_redirect_post_login(self):
        self.client.post('/accounts/login/', {'username': 'testuser', 'password': 'secret'})
        response = self.client.get('/accounts/login/')
        self.assertRedirects(response, reverse('index'))

class TestLogoutBehaviour(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        User.objects.create_user(**self.credentials)
        self.client.post('/accounts/login/', {'username': 'testuser', 'password': 'secret'}, follow=True)

    """
    Using in app method to login instead of direct login.
    """
    def test_logout(self):
        response = self.client.get('/accounts/logout/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout_redirect(self):
        response = self.client.get('/accounts/logout/', follow=True)
        self.assertRedirects(response, reverse('index'))

    def test_login_message(self):
        response = self.client.get('/accounts/logout/', follow=True)
        self.assertContains(response, 'You have successfully logged out.')

class TestRegistrationView(TestCase):
    def test_view_status(self):
        response = self.client.get('/accounts/register/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('registration'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('registration'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/accounts/register/')
        self.assertContains(response, '<h1>User Registration</h1>')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/accounts/register/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

class TestRegistrationBehaviour(TestCase):
    def test_registration(self):
        response = self.client.post(
            reverse('registration'),
            data = {
                'username': 'testuser',
                'email': 'test@test.com',
                'password1': 'kakapapa',
                'password2': 'kakapapa'
            })
        user = User.objects.get(username='testuser')
        self.assertTrue(user.is_authenticated)

    def test_registration_redirect(self):
        response = self.client.post(
            reverse('registration'),
            data = {
                'username': 'testuser',
                'email': 'test@test.com',
                'password1': 'kakapapa',
                'password2': 'kakapapa'
            }, follow=True)
        self.assertRedirects(response, reverse('index'))

    def test_registration_message(self):
        response = self.client.post(
            reverse('registration'),
            data = {
                'username': 'testuser',
                'email': 'test@test.com',
                'password1': 'kakapapa',
                'password2': 'kakapapa'
            }, follow=True)
        self.assertContains(response, 'You have successfully registered!')

    """
    This test checks that user will not be directed to registration page after
    registration and logged in.
    """
    def test_redirect_post_login(self):
        self.client.post(
            reverse('registration'),
            data = {
                'username': 'testuser',
                'email': 'test@test.com',
                'password1': 'kakapapa',
                'password2': 'kakapapa'
            }, follow=True)
        response = self.client.get(reverse('registration'))
        self.assertRedirects(response, reverse('index'))

class TestProfileView(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        User.objects.create_user(**self.credentials)
        self.client.post('/accounts/login/', {'username': 'testuser', 'password': 'secret'})

    def test_view_status(self):
        response = self.client.get('/accounts/profile/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/accounts/profile/')
        self.assertContains(response, '<h1>testuser Profile</h1>')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/accounts/profile/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')
