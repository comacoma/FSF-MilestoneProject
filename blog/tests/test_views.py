from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post

class TestBlogHomeView(TestCase):
    def test_view_status(self):
        response = self.client.get('/blog/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('blog_home'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blog_home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bloghome.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/blog/')
        self.assertContains(response, 'Unicorn Attractor Blogs')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/blog/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

class TestUserBlogHomeView(TestCase):
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
        response = self.client.get('/blog/myblogs/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('user_blog_home'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('user_blog_home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bloghome.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/blog/myblogs/')
        self.assertContains(response, 'testuser Blogs')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/blog/myblogs/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

class TestBlogPostDetailViewAndBehaviour(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        User.objects.create_user(**cls.credentials)

        Post.objects.create(
            author=User.objects.get(pk=1),
            title='Test Post',
            content='test content.'
        )

    def setUp(self):
        self.client.login(username='testuser', password='secret')

    def test_view_status(self):
        response = self.client.get('/blog/1/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk':1}))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk':1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'postdetail.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/blog/1/')
        self.assertContains(response, 'Test Post')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/blog/1/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

    def test_view_count(self):
        response = self.client.get('/blog/1/')
        post = Post.objects.get(pk=1)
        view_count = post.views
        self.assertEquals(view_count, 1)

class TestNewBlogPostViewAndBehaviour(TestCase):
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
        response = self.client.get('/blog/new/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('new_post'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('new_post'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogpostform.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/blog/new/')
        self.assertContains(response, 'New Post')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/blog/new/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

    def test_redirect_post_submit(self):
        response = self.client.post(
            '/blog/new/',
            data={
                'author': 1,
                'title': 'test title'
            }
        )
        self.assertRedirects(response, '/blog/1/')

class TestEditBlogPostViewAndBehaviour(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        User.objects.create_user(**cls.credentials)

        Post.objects.create(
            author=User.objects.get(pk=1),
            title='Test Post',
            content='test content.'
        )

    def setUp(self):
        self.client.login(username='testuser', password='secret')

    def test_view_status(self):
        response = self.client.get('/blog/1/edit/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('edit_post', kwargs={'pk':1}))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('edit_post', kwargs={'pk':1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogpostform.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/blog/1/edit/')
        self.assertContains(response, 'Edit Post')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/blog/1/edit/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

    def test_redirect_post_submit(self):
        response = self.client.post(
            '/blog/1/edit/',
            data={
                'author': 1,
                'title': 'test title updated'
            }
        )
        self.assertRedirects(response, '/blog/1/')
