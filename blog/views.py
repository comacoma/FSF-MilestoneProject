from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from .forms import BlogPostForm

# Create your views here.
def blog_home(request):
    """
    A view that serves as the home page of blog feature. All blog
    entries of all users will be displayed here.
    """

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, "bloghome.html", {'posts': posts})
