from django.test import TestCase
from django.contrib.auth.models import User
from issuetracker.models import Ticket, Comment, Fund, ProgressLog
from django.utils import timezone

"""
To test if models used in issuetracker app are stored correctly.
"""
class TestTicketModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email='testuser@user.com',
            username='testuser',
            password='tatavava'
        )

        Ticket.objects.create(
            title='test ticket title',
            type='T1',
            author=User.objects.get(pk=1),
            content='unlike blog, content is required in ticket',
        )

    def test_model_content(self):
        ticket = Ticket.objects.get(pk=1)
        self.assertEquals(f'{ticket.author.username}', 'testuser')
        self.assertEquals(f'{ticket.title}', 'test ticket title')
        self.assertEquals(f'{ticket.type}', 'T1')
        self.assertEquals(f'{ticket.content}', 'unlike blog, content is required in ticket')
        self.assertEquals(f'{ticket.status}', 'S1') # testing default value
        self.assertEquals(f'{ticket.upvote_user}', 'auth.User.None') # testing default value/ string representation of default value
        self.assertEquals(f'{ticket.upvote_fund}', '0.00') # testing default value/ string representation of default value
        self.assertEquals(ticket.__str__(), ticket.title)
        self.assertEquals(ticket.get_absolute_url(), '/issuetracker/ticket/1/')

class TestCommentModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email='testuser@user.com',
            username='testuser',
            password='tatavava'
        )

        Ticket.objects.create(
            title='test ticket title',
            type='T1',
            author=User.objects.get(pk=1),
            content='unlike blog, content is required in ticket'
        )

        Comment.objects.create(
            ticket=Ticket.objects.get(pk=1),
            author=User.objects.get(pk=1),
            content='test comment content'
        )

    def test_model_content(self):
        comment = Comment.objects.get(pk=1)
        comment_date = comment.comment_date.strftime('%Y-%m-%d %H:%M:%S') # default value defined by model
        self.assertEquals(f'{comment.author.username}', 'testuser')
        self.assertEquals(f'{comment.ticket.title}', 'test ticket title')
        self.assertEquals(f'{comment.content}', 'test comment content')
        self.assertEquals(
            comment.__str__(),
            'testuser @ ' + comment_date + ' ON test ticket title'
        )

class TestFundModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email='testuser@user.com',
            username='testuser',
            password='tatavava'
        )

        Ticket.objects.create(
            title='test ticket title',
            type='T2',
            author=User.objects.get(pk=1),
            content='unlike blog, content is required in ticket'
        )

        Fund.objects.create(
            ticket=Ticket.objects.get(pk=1),
            user=User.objects.get(pk=1),
            fund=1,
            date='2018-10-07T14:00:00Z'
        )

    def test_model_content(self):
        fund_log = Fund.objects.get(pk=1)
        fund_log_date = fund_log.date.strftime('%Y-%m-%d %H:%M:%S')
        self.assertEquals(f'{fund_log.ticket.title}', 'test ticket title')
        self.assertEquals(f'{fund_log.user.username}', 'testuser')
        self.assertEquals(f'{fund_log.fund}', '1.00')
        self.assertEquals(
            fund_log.__str__(),
            '£1.00 by testuser ON test ticket title / Date:' + fund_log_date
        )

class TestProgressLog(TestCase):
    @classmethod
    def setUpTestData(cls):
        ProgressLog.objects.create(
            date='2018-10-07',
            bug_tended=0,
            feature_tended=0,
        )

    def test_model_content(self):
        progress_log = ProgressLog.objects.get(pk='2018-10-07')
        self.assertEquals(f'{progress_log.bug_tended}', '0')
        self.assertEquals(f'{progress_log.feature_tended}', '0')
        self.assertEquals(
            progress_log.__str__(),
            '2018-10-07: Bug Tended: 0 // Feature Request Tended: 0'
        )
