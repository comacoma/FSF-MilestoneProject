from django.db import models
from django.conf import settings

# Create your models here.
class Ticket(models.Model):
    BUG = 'T1'
    FEATURE_REQUEST = 'T2'
    CATEGORY = (
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
    type = models.CharField(max_length=2, choices=CATEGORY, default=BUG)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.PROTECT,
    )
    content = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS, default=REVIEWING)
    threshold = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

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
    comment_date = models.DateTimeField(auto_now_add=True)
