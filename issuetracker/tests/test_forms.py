from django.test import TestCase
from django.contrib.auth.models import User
from issuetracker.models import Ticket, Comment
from issuetracker.forms import (
    TicketSubmitForm,
    CommentPostForm,
    FundingForm,
    UpdateStatusForm,
    UpdateThresholdForm,
    CardDetailForm
)

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
