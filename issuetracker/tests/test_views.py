from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from issuetracker.models import Ticket, Comment, Fund, ProgressLog
from issuetracker.forms import (
    TicketSubmitForm,
    CommentPostForm,
    FundingForm,
    UpdateStatusForm,
    UpdateThresholdForm,
    CardDetailForm
)

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

class TestCommentEditFormView(TestCase):
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

        Comment.objects.create(
            author=User.objects.get(pk=1),
            ticket=Ticket.objects.get(pk=1),
            content='test comment'
        )

    def setUp(self):
        self.client.login(username='testuser', password='secret')

    def test_view_status(self):
        response = self.client.get('/issuetracker/ticket/1/comment/1/edit/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('edit_comment', kwargs={'ticketpk':1, 'commentpk':1}))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('edit_comment', kwargs={'ticketpk':1, 'commentpk':1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'commenteditform.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/issuetracker/ticket/1/comment/1/edit/')
        self.assertContains(response, '<title>Unicorn Attractor - Issue Tracker - Edit Comment</title>')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/issuetracker/ticket/1/comment/1/edit/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

class TestTicketBehaviour(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        User.objects.create_user(**cls.credentials)

    def setUp(self):
        self.client.login(username='testuser', password='secret')

    def test_ticket_submission(self):
        response = self.client.post(
            reverse('submit_new_ticket'),
            data={
                'author': 1,
                'title': 'test ticket title',
                'content': 'test ticket content',
                'type': 'T1',
            }
        )
        self.assertRedirects(response, reverse('ticket_details', kwargs={'pk':1}))

    def test_ticket_edit(self):
        Ticket.objects.create(
            author=User.objects.get(username='testuser'),
            title='test ticket title 1',
            content='test ticket content',
            type='T1',
        )
        response = self.client.post(
            reverse('edit_ticket', kwargs={'pk':1}),
            data={
                'title': 'test ticket title 2',
                'content': 'test ticket content',
            },
            follow=True
        )
        self.assertRedirects(response, reverse('ticket_details', kwargs={'pk':1}))
        self.assertContains(response, 'test ticket title 2')
        self.assertNotContains(response, 'test ticket title 1')

    def test_unauthorised_ticket_edit(self):
        new_user = User.objects.create_user('user2')
        new_user.set_password('12345')
        new_user.save()

        # test user submitted a ticket
        self.client.post(
            reverse('submit_new_ticket'),
            data={
                'author': 1,
                'title': 'test ticket title 1',
                'content': 'test ticket content',
                'type': 'T1',
            }
        )

        self.client.logout() # logout testuser who posted the ticket
        self.client.login(username='user2', password='12345') # login newly created user2

        response = self.client.post(
            reverse('edit_ticket', kwargs={'pk':1}),
            data={
                'title': 'test ticket title 2', # user2 is attempting to edit the ticket
                'content': 'test ticket content',
            },
            follow=True
        )
        # to check that user2 has been redirected, thus the post request did not go through
        self.assertRedirects(response, reverse('ticket_details', kwargs={'pk':1}))
        self.assertContains(response, 'You are not the author of this ticket and thus not allowed to edit.')
        self.assertContains(response, 'test ticket title 1')
        self.assertNotContains(response, 'test ticket title 2')

class TestCommentBehaviour(TestCase):
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
            content='test content.',
            type='T1'
        )

    def setUp(self):
        self.client.login(username='testuser', password='secret')

    def test_comment_submission(self):
        response = self.client.post(
            reverse('ticket_details', kwargs={'pk':1}),
            data={
                'author': 1,
                'ticket': 1,
                'content': 'test comment',
                'comment_date': '2018-10-07 14:00:00',
            },
            follow=True
        )
        self.assertRedirects(response, reverse('ticket_details', kwargs={'pk':1}))
        self.assertContains(response, 'test comment')

    def test_comment_edit(self):
        Comment.objects.create(
            ticket=Ticket.objects.get(pk=1),
            author=User.objects.get(username='testuser'),
            content='test comment 1'
        )
        response = self.client.post(
            reverse('edit_comment', kwargs={'ticketpk': 1, 'commentpk': 1}),
            data={
                'author': 1,
                'ticket': 1,
                'content': 'test comment 2'
            },
            follow=True
        )
        self.assertRedirects(response, reverse('ticket_details', kwargs={'pk':1}))
        self.assertContains(response, 'test comment 2')
        self.assertNotContains(response, 'test comment 1')

    def test_unauthorised_comment_edit(self):
        Comment.objects.create(
            ticket=Ticket.objects.get(pk=1),
            author=User.objects.get(username='testuser'),
            content='test comment 1'
        )

        new_user = User.objects.create_user('user2')
        new_user.set_password('12345')
        new_user.save()

        self.client.logout() # logout testuser who posted the ticket
        self.client.login(username='user2', password='12345') # login newly created user2

        response = self.client.post(
            reverse('edit_comment', kwargs={'ticketpk': 1, 'commentpk': 1}),
            data={
                'content': 'test comment 2', # user2 attempting to edit a comment posted by testuser
            },
            follow=True
        )
        # to check that user2 has been redirected, thus the post request did not go through
        self.assertRedirects(response, reverse('ticket_details', kwargs={'pk':1}))
        self.assertContains(response, 'You are not the author of the comment and thus not allowed to edit.')
        self.assertContains(response, 'test comment 1')
        self.assertNotContains(response, 'test comment 2')

    def test_invalid_comment_retrieval(self):
        # creating a second ticket
        Ticket.objects.create(
            author=User.objects.get(pk=1),
            title='Test Post 2',
            content='test content.',
            type='T1'
        )

        # creating a comment for the ticket above
        Comment.objects.create(
            ticket=Ticket.objects.get(pk=2),
            author=User.objects.get(username='testuser'),
            content='test comment 1 for Test Post 2'
        )

        response = self.client.post(
            reverse('edit_comment', kwargs={'ticketpk': 1, 'commentpk':1}),
            data={
                'content': 'test comment 2 for Test Post', # attempting to edit a comment that does not belong to ticket with pk=1
            },
            follow=True
        )
        self.assertRedirects(response, reverse('ticket_details', kwargs={'pk':1}))
        self.assertContains(response, 'Comment retrieved is not part of this ticket, please check your url.')
        self.assertNotContains(response, 'test comment 1')
        self.assertNotContains(response, 'test comment 2')

class TestUpdateTicketDetails(TestCase):
    @classmethod
    def setUpTestData(cls):
        new_staff = User.objects.create_user('teststaff')
        new_staff.set_password('12345')
        new_staff.is_staff = True
        new_staff.save()

        new_user = User.objects.create_user('testuser')
        new_user.set_password('secret')
        new_user.save()

        Ticket.objects.create(
            author=User.objects.get(pk=1),
            title='Test Post (Bug)',
            content='test content.',
            type='T1'
        )

        Ticket.objects.create(
            author=User.objects.get(pk=1),
            title='Test Post (Feature Request)',
            content='test content.',
            type='T2'
        )

    def test_update_ticket_status(self):
        self.client.login(username='teststaff', password='12345')
        response = self.client.post(
            reverse('update_status', kwargs={'pk':1}),
            data={
                'status': 'S2'
            },
            follow=True
        )
        self.assertRedirects(response, reverse('ticket_details', kwargs={'pk':1}))
        self.assertContains(
            response,
            '<option value="S2" selected>To Do</option>'
        )
        self.assertNotContains(
            response,
            '<option value="S1" selected>Reviewing</option>'
        )

    def test_update_ticket_threshold(self):
        self.client.login(username='teststaff', password='12345')
        response = self.client.post(
            reverse('update_threshold', kwargs={'pk':1}),
            data={
                'threshold': 10
            },
            follow=True
        )
        ticket = Ticket.objects.get(pk=1)
        self.assertRedirects(response, reverse('ticket_details', kwargs={'pk':1}))
        self.assertEquals(ticket.threshold, 10)

    def test_invalid_update_ticket_status(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.post(
            reverse('update_status', kwargs={'pk':1}),
            data={
                'status': 'S2'
            },
            follow=True
        )
        ticket = Ticket.objects.get(pk=1)
        self.assertRedirects(
            response,
            # redirected to admin login page (i.e. user need to be a staff to update ticket status)
            '/admin/login/?next=/issuetracker/ticket/1/update_status/'
        )
        self.assertEquals(ticket.status, 'S1') # post request failed as expected

    def test_invalid_update_ticket_threshold(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.post(
            reverse('update_threshold', kwargs={'pk':1}),
            data={
                'threshold': 10
            },
            follow=True
        )
        ticket = Ticket.objects.get(pk=1)
        self.assertRedirects(
            response,
            # redirected to admin login page (i.e. user need to be a staff to update threshold)
            '/admin/login/?next=/issuetracker/ticket/1/update_threshold/'
        )
        self.assertEquals(ticket.threshold, None) # post request failed as expected

class TestUpvoteBehaviour(TestCase):
    @classmethod
    def setUpTestData(cls):
        new_staff = User.objects.create_user('teststaff')
        new_staff.set_password('12345')
        new_staff.is_staff = True
        new_staff.save()

        new_user = User.objects.create_user('testuser')
        new_user.set_password('secret')
        new_user.save()

        Ticket.objects.create(
            author=User.objects.get(pk=1),
            title='Test Post (Bug)',
            content='test content.',
            type='T1'
        )

    def setUp(self):
        self.client.login(username='teststaff', password='12345')

    def test_bug_upvote(self):
        ticket = Ticket.objects.get(pk=1)
        self.assertFalse(ticket.upvote_user.exists()) # no one has upvote the ticket yet
        response = self.client.post(reverse('upvote', kwargs={'pk':1}))
        ticket = Ticket.objects.get(pk=1)
        self.assertRedirects(response, reverse('ticket_details', kwargs={'pk':1}))
        self.assertTrue(ticket.upvote_user.exists()) # there is at least one user upvoted this ticket

    def test_undo_bug_upvote(self):
        response = self.client.post(reverse('upvote', kwargs={'pk':1})) # upvote
        response = self.client.post(reverse('upvote', kwargs={'pk':1})) # undo upvote
        ticket = Ticket.objects.get(pk=1)
        self.assertRedirects(response, reverse('ticket_details', kwargs={'pk':1}))
        self.assertFalse(ticket.upvote_user.exists())

    def test_invalid_url(self):
        """
        To test that user should not be able to get to a 'funding page'
        of a bug ticket.
        """
        response = self.client.get(reverse('fund', kwargs={'pk':1}), follow=True)
        self.assertRedirects(response, reverse('ticket_details', kwargs={'pk':1}))
        self.assertContains(
            response,
            'You upvote is all we need to work on a bug fixes.' +
            ' We appreciate the thought though!'
        )

    def test_auto_update_ticket_status(self):
        ticket = Ticket.objects.get(pk=1)
        ticket.threshold = 2
        ticket.save()
        self.assertEquals(ticket.status, 'S1')
        self.client.post(reverse('upvote', kwargs={'pk':1})) # upvote by teststaff
        self.client.logout()
        self.client.login(username='testuser', password='secret')
        self.client.post(reverse('upvote', kwargs={'pk':1}), follow=True) # upvote by testuser
        ticket = Ticket.objects.get(pk=1)
        self.assertEquals(ticket.status, 'S2') # status has been updated automatically

class TestFundBehaviour(TestCase):
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

    def setUp(self):
        self.client.login(username='teststaff', password='12345')

    def test_invalid_url(self):
        """
        To test that user should not be able to get to a 'funding page'
        of a bug ticket.
        """
        response = self.client.get(reverse('upvote', kwargs={'pk':1}), follow=True)
        self.assertRedirects(response, reverse('ticket_details', kwargs={'pk':1}))
        self.assertContains(
            response,
            'Upvoting alone is not enough. We need your donation so that we can' +
            ' work on the feature request!'
        )
