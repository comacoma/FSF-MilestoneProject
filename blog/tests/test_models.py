from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post
from django.utils import timezone

"""
To test if blog post objects are stored correctly.
"""
class TestPostModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email='user1@user.com',
            username='user1',
            password='tatavava'
        )

        Post.objects.create(
            author=User.objects.get(pk=1),
            title='Test Post',
            content='test content.'
        )

    def test_model_content(self):
        post = Post.objects.get(id=1)
        self.assertEquals(f'{post.author.username}', 'user1')
        self.assertEquals(f'{post.title}', 'Test Post')
        self.assertEquals(f'{post.content}', 'test content.')
        self.assertEquals(post.__str__(), 'Test Post BY user1')
        self.assertEquals(post.__unicode__(), post.title)
