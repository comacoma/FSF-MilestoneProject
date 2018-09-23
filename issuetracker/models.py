from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator

# Create your models here.
class Ticket(models.Model):
    BUG = 'T1'
    FEATURE_REQUEST = 'T2'
    TYPE = (
        (BUG, 'Bug'),
        (FEATURE_REQUEST, 'Feature Request'),
    )

    REVIEWING = 'S1'
    TODO = 'S2'
    DOING = 'S3'
    DONE = 'S4'
    ONHOLD = 'S5'
    STATUS = (
        (REVIEWING, 'Reviewing'),
        (TODO, 'To Do'),
        (DOING, 'Doing'),
        (DONE, 'Done'),
        (ONHOLD, 'On Hold'),
    )

    title = models.CharField(max_length=50, blank=False)
    type = models.CharField(max_length=2, choices=TYPE, default=BUG)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.PROTECT,
    )
    content = models.TextField()
    submission_date = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now)
    status = models.CharField(max_length=2, choices=STATUS, default=REVIEWING)
    upvote_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name = 'upvoted',
        blank = True,
        default = None
    )
    upvote_fund = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=0)
    threshold = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ticket_details', args=[str(self.id)])

class Comment(models.Model):
    ticket = models.ForeignKey(
        'Ticket',
        on_delete = models.PROTECT,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.PROTECT,
    )
    content = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{0} @ {1} ON {2}".format(self.author.username, self.comment_date.strftime('%Y-%m-%d %H:%M:%S'), self.ticket.title)

class Fund(models.Model):
    ticket = models.ForeignKey(
        'Ticket',
        on_delete = models.PROTECT,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.PROTECT,
    )
    fund = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=False,
        null=False,
        default=1,
        validators=[MinValueValidator(1)],
    )
    date = models.DateTimeField()

    def __str__(self):
        return "£{0} by {1} ON {2}".format(self.fund, self.user.username, self.date.strftime('%Y-%m-%d %H:%M:%S'))
