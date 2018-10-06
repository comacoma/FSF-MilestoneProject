from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    """A single blog post"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.PROTECT,
    )
    """
    Content can be left blank but title is required
    """
    title = models.CharField(max_length=200, blank=False, null=False)
    content = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    views = models.IntegerField(default=0)
    tag = models.CharField(max_length=30, blank=True, null=True)
    image = models.ImageField(upload_to="img", blank=True, null=True)

    def __str__(self):
        return "{0} BY {1}".format(self.title, self.author)

    def __unicode__(self):
        return self.title
