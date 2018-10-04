from django.test import TestCase
from django.urls import reverse

"""
Home app does not have any data model directly
related to it so it is not needed to setup
test data.

The same can be said for functionality as views in home app
are used to render templates ONLY in this case.
"""

class TestIndexViews(TestCase):
    def test_view_status(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/')
        self.assertContains(
            response, '<h2>Welcome to Unicorn Attractor, your one stop web service for getting your very own unicorn!</h2>')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')

class TestAboutViews(TestCase):
    def test_view_status(self):
        response = self.client.get('/about/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('about'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('about'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/about/')
        self.assertContains(
            response,
            '<h1>About Unicorn Attractor</h1>')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/about/')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')
