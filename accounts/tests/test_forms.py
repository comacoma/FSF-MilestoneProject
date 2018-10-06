from django.test import TestCase
from accounts.forms import *
from django.contrib.auth.models import User

"""
These tests only test if the form validates input, but
does not test the behaviour related to using the forms.
"""
class TestUserLoginForm(TestCase):
    def test_form(self):
        form_data = {
            'username': 'testuser',
            'password': 'secret'
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_1(self):
        form_data = {
            'username': 'testuser',
            'password': '' # No password entry
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_2(self):
        form_data = {
            'username': '', # No username entry
            'password': 'something'
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

class TestUserRegistrationForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email='user1@user.com',
            username='user1',
            password='tatavava'
        )

    def test_form(self):
        form_data = {
            'email': 'test@test.com',
            'username': 'testuser',
            'password1': 'kakapapa',
            'password2': 'kakapapa'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test__invalid_form_1(self):
        form_data = {
            'email': 'test@test.com',
            'username': 'testuser',
            'password1': 'secret', # password too simple
            'password2': 'secret'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test__invalid_form_2(self):
        form_data = {
            'email': 'test@test.com',
            'username': 'testuser',
            'password1': 'kakapapa',
            'password2': 'lalababa' # passwords are not the same
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test__invalid_form_3(self):
        form_data = {
            'email': 'this is not a email address', # not a valid email format
            'username': 'testuser',
            'password1': 'kakapapa',
            'password2': 'kakapapa'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test__invalid_form_4(self):
        form_data = {
            'email': 'test@test.com',
            'username': 'user1', # using existing username
            'password1': 'kakapapa',
            'password2': 'kakapapa'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test__invalid_form_5(self):
        form_data = {
            'email': 'user1@user.com', # using existing email
            'username': 'testuser',
            'password1': 'kakapapa',
            'password2': 'kakapapa'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
