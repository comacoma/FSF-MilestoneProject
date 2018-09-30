from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Post
from .forms import BlogPostForm
from .filters import BlogPostFilter

# Create your views here.
def blog_home(request):
    """
    A view that serves as the home page of blog feature. All blog
    entries of all users will be displayed here.
    """

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    filter = BlogPostFilter(request.GET, queryset=posts)
    paginator = Paginator(filter.qs, 20)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, "bloghome.html", {'posts': posts, 'filter': filter})

@login_required
def user_blog_home(request):
    posts = Post.objects.filter(author=request.user).order_by('-published_date')
    filter = BlogPostFilter(request.GET, queryset=posts)
    paginator = Paginator(filter.qs, 20)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, "bloghome.html", {'posts': posts, 'filter': filter})

def post_detail(request, pk):
    """
    Create a view that returns a single
    Post object based on the post ID (pk) and
    render it to the 'postdetail.html' template
    or renturn a 404 error if the post is not found
    """

    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    return render(request, "postdetail.html", {'post': post})

@login_required
def create_or_edit_post(request, pk=None):
    """
    Create a view that allows us to
    create or edit a post depending if that Post ID
    is null or not
    """

    authorid = request.user.id if request.user.is_authenticated else None

    post = get_object_or_404(Post, pk=pk) if pk else None
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostForm(instance=post, initial={'author': authorid})
    return render(request, "blogpostform.html", {'form': form})
