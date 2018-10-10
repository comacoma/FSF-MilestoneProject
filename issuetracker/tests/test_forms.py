from django.test import TestCase
from django.contrib.auth.models import User
from issuetracker.models import Ticket, Comment
from issuetracker.forms import (
    TicketSubmitForm,
    CommentPostForm,
    FundingForm,
    CardDetailForm
)

from unicorn_attractor.settings import STRIPE_SECRET
import stripe

"""
To test if forms used in issuetracker app behaves as expected.
"""
class TestTicketSubmitForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email='testuser@user.com',
            username='testuser',
            password='tatavava'
        )

    def test_form(self):
        form_data = {
            'author': 1,
            'last_modified': '2018-10-07 14:00:00',
            'type': 'T1',
            'title': 'test ticket title',
            'content': 'test ticket content',
        }
        form = TicketSubmitForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_1(self):
        form_data = {
            'author': 1,
            'last_modified': '2018-10-07 14:00:00',
            'type': 'T1',
            'title': '', # no title
            'content': 'test ticket content',
        }
        form = TicketSubmitForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_2(self):
        form_data = {
            'author': 1,
            'last_modified': '2018-10-07 14:00:00',
            'type': 'T1',
            'title': 'test ticket title',
            'content': '', # no content
        }
        form = TicketSubmitForm(data=form_data)
        self.assertFalse(form.is_valid())

class TestCommentForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email='testuser@user.com',
            username='testuser',
            password='tatavava'
        )

        Ticket.objects.create(
            author=User.objects.get(username='testuser'),
            title='test ticket title',
            content='test ticket content',
            type='T1',
        )

    def test_form(self):
        form_data = {
            'author': 1,
            'ticket': 1,
            'last_modified': '2018-10-07 14:00:00',
            'content': 'test comment',
        }
        form = CommentPostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_1(self):
        form_data = {
            'author': 1,
            'ticket': 1,
            'last_modified': '2018-10-07 14:00:00',
            'content': '', # comment is empty
        }
        form = CommentPostForm(data=form_data)
        self.assertFalse(form.is_valid())

class TestFundingForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        new_staff = User.objects.create_user('teststaff')
        new_staff.set_password('12345')
        new_staff.is_staff = True
        new_staff.save()

        Ticket.objects.create(
            author=User.objects.get(pk=1),
            title='Test Post (Bug)',
            content='test content.',
            type='T2'
        )

        stripe.api_key = STRIPE_SECRET

    def test_form(self):
        form_data={
            'user': 1,
            'ticket': 1,
            'fund': 10
        }
        form = FundingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_1(self):
        form_data={
            'user': 1,
            'ticket': 1,
            'fund': 0.9 # fund < 1.0
        }
        form = FundingForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_2(self):
        form_data={
            'user': 1,
            'ticket': 1,
            'fund': '' # empty
        }
        form = FundingForm(data=form_data)
        self.assertFalse(form.is_valid())

class TestCardDetailForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        new_staff = User.objects.create_user('teststaff')
        new_staff.set_password('12345')
        new_staff.is_staff = True
        new_staff.save()

        Ticket.objects.create(
            author=User.objects.get(pk=1),
            title='Test Post (Bug)',
            content='test content.',
            type='T2'
        )

    def test_form(self):
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2020,
                "cvc": '123'
            },
        )

        form_data={
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': 12,
            'expiry_year': 2020,
            'stripe_id': token.id
        }
        form = CardDetailForm(data=form_data)
        self.assertTrue(form.is_valid())
