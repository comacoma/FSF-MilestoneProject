from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import TicketPostForm

# Create your views here.
def issuetrackerhome(request):
    return render(request, "issue_tracker_home.html")

@login_required
def submitnewticket(request):
    form = TicketPostForm
    author = request.user.username if request.user.is_authenticated else None
    return render(request, "ticket_post_form.html", {'form': form, 'author': author})
