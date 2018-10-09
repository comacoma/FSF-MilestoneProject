from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from issuetracker.models import Ticket, Comment, Fund, ProgressLog

class TestIssueTrackerHomeView(TestCase):
    def test_view_status(self):
        response = self.client.get('/issuetracker/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('issue_tracker_home'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('issue_tracker_home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'issuetrackerhome.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/issuetracker/')
        self.assertContains(response, '<h1>Issue Tracker - Home Page</h1>')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/issuetracker/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

class TestTicketRankingProgressView(TestCase):
    def test_view_status(self):
        response = self.client.get('/issuetracker/ticket_ranking_progress/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('ticket_ranking_progress'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('ticket_ranking_progress'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticketrankingprogress.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/issuetracker/ticket_ranking_progress/')
        self.assertContains(response, '<h1>Issue Tracker - Ticket Rankings and Progress</h1>')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/issuetracker/ticket_ranking_progress/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

class TestTicketSubmitFormView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        User.objects.create_user(**cls.credentials)

    def setUp(self):
        self.client.login(username='testuser', password='secret')

    def test_view_status(self):
        response = self.client.get('/issuetracker/ticket/new/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('submit_new_ticket'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('submit_new_ticket'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticketpostform.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/issuetracker/ticket/new/')
        self.assertContains(response, '<h1>Issue Tracker - Submit New Ticket</h1>')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/issuetracker/ticket/new/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

class TestTicketDetailsViewAndBehaviour(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email='testuser@user.com',
            username='testuser',
            password='tatavava'
        )

        Ticket.objects.create(
            author=User.objects.get(pk=1),
            title='Test Post',
            content='test content.'
        )

    def test_view_status(self):
        response = self.client.get('/issuetracker/ticket/1/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('ticket_details', kwargs={'pk':1}))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('ticket_details', kwargs={'pk':1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticketdetails.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/issuetracker/ticket/1/')
        self.assertContains(response, 'Test Post')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/issuetracker/ticket/1/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

class TestTicketEditFormView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        User.objects.create_user(**cls.credentials)

        Ticket.objects.create(
            author=User.objects.get(pk=1),
            title='Test Post',
            content='test content.'
        )

    def setUp(self):
        self.client.login(username='testuser', password='secret')

    def test_view_status(self):
        response = self.client.get('/issuetracker/ticket/1/edit/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('edit_ticket', kwargs={'pk':1}))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('edit_ticket', kwargs={'pk':1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticketeditform.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/issuetracker/ticket/1/edit/')
        self.assertContains(response, '<title>Unicorn Attractor - Issue Tracker - Edit Ticket</title>')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/issuetracker/ticket/1/edit/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

class TestTicketSubmitBehaviour(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        User.objects.create_user(**cls.credentials)

    def setUp(self):
        self.client.login(username='testuser', password='secret')

    def test_redirect_post_ticket_submission(self):
        response = self.client.post(
            reverse('submit_new_ticket'),
            data={
                'author': 1,
                'title': 'test ticket title',
                'content': 'test ticket content',
                'type': 'T1',
                'last_modified': '2018-10-09 10:00:00'
            }
        )
        self.assertRedirects(response, reverse('ticket_details', kwargs={'pk':1}))

class TestCommentSubmitBehaviour(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        User.objects.create_user(**cls.credentials)

        Ticket.objects.create(
            author=User.objects.get(pk=1),
            title='Test Post',
            content='test content.'
        )

    def setUp(self):
        self.client.login(username='testuser', password='secret')

    def test_comment_submission(self):
        response = self.client.post(
            reverse('ticket_details', kwargs={'pk':1}),
            data={
                'author': User.objects.get(pk=1),
                'ticket': Ticket.objects.get(pk=1),
                'content': 'test comment'
            },
        )
        self.assertContains(response, 'test comment')
