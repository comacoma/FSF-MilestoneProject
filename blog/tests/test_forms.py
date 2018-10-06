from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from blog.models import Post
from blog.forms import BlogPostForm

"""
To test if blog post form behaves as expected.
"""
class TestBlogPostForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email='user1@user.com',
            username='user1',
            password='tatavava'
        )

    def test_form(self):
        form_data = {
            'author': 1, # Id of user
            'title': 'test title'
        }
        form = BlogPostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_1(self):
        form_data = {
            'author': 1,
            'title': None # No title
        }
        form = BlogPostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_2(self):
        form_data = {
            'author': 1,
            'title': 'a' * 201 # over max length
        }
        form = BlogPostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_3(self):
        form_data = {
            'author': 1,
            'title': 'test title',
            'tag': 'a' * 31 # over max length
        }
        form = BlogPostForm(data=form_data)
        self.assertFalse(form.is_valid())
