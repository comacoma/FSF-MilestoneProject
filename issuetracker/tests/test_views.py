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
