from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Ticket, Comment, Fund
from .forms import TicketSubmitForm, CommentPostForm, FundSubmitForm, UpdateStatusForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import HttpResponse

# Create your views here.
def issue_tracker_home(request):
    tickets = Ticket.objects.all().order_by('-submission_date')
    paginator = Paginator(tickets, 20)
    page = request.GET.get('page')
    tickets = paginator.get_page(page)
    return render(request, "issuetrackerhome.html", {'tickets': tickets})

@login_required
def submit_new_ticket(request):
    """
    A view that displays the form for submitting new ticket.
    User will only need to fill in category of ticket, title and
    content in order to submit a ticket as other attributes can and should
    be adjusted after a ticket entity is created.
    """

    authorid = request.user.id if request.user.is_authenticated else None
    author = request.user.username if request.user.is_authenticated else None
    if request.method == "POST":
        form = TicketSubmitForm(request.POST)
        if form.is_valid():
            ticket = form.save()
            return redirect(ticket_details, ticket.id)
    else:
        form = TicketSubmitForm(initial={'author': authorid})
    return render(request, "ticketpostform.html", {'form': form, 'author': author})

def ticket_details(request, pk):
    """
    A view that displays the details of a particular ticket,
    as well as providing area for fellow users to comment.
    """

    authorid = request.user.id if request.user.is_authenticated else None

    ticket = get_object_or_404(Ticket, pk=pk)
    status = UpdateStatusForm(instance=ticket)
    comments = Comment.objects.filter(ticket=ticket).order_by('-comment_date')
    paginator = Paginator(comments, 10)
    page = request.GET.get('page')
    comments = paginator.get_page(page)
    upvoted_user = ticket.upvote_user.all()

    if request.method == "POST":
        form = CommentPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(ticket_details, ticket.id)
    else:
        form = CommentPostForm(initial={'author': authorid, 'ticket': ticket.id})
    return render(
        request,
        'ticketdetails.html',
        {
            'ticket': ticket,
            'comments': comments,
            'form': form,
            'upvoted_user': upvoted_user,
            'status': status,
        })

def edit_ticket(request, pk):
    """
    A view that allows users to edit existing tickets
    """

    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == "POST":
        form = TicketSubmitForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            return redirect(ticket_details, ticket.pk)
    else:
        form = TicketSubmitForm(instance=ticket, initial={'last_modified': timezone.now})
    return render(request, 'ticketeditform.html', {'form': form, 'ticket': ticket})

def edit_comment(request, ticketpk, commentpk):
    """
    A view that allows user to edit comment they posted
    on a particular ticket.
    """

    ticket = get_object_or_404(Ticket, pk=ticketpk)
    comment = get_object_or_404(Comment, pk=commentpk)

    if request.method == "POST":
        form = CommentPostForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(ticket_details, ticket.pk)
    else:
        form = CommentPostForm(instance=comment)
    return render(request, 'commenteditform.html', {'form': form, 'ticket': ticket})

@login_required
def upvote(request, pk):
    """
    A functional view that adds or remove a user's upvote to a ticket.
    """
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.upvote_user.filter(id=request.user.id).exists():
        ticket.upvote_user.remove(request.user)
        return redirect(ticket_details, ticket.pk)
    else:
        ticket.upvote_user.add(request.user)
        return redirect(ticket_details, ticket.pk)

@login_required
def fund(request, pk):
    """
    A view that displays a form for paying towards a feature request ticket.
    """
    ticket = get_object_or_404(Ticket, pk=pk)
    form = FundSubmitForm()
    return render(request, 'ticketfundingform.html', {'ticket': ticket, 'form': form})

@staff_member_required
def update_status(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    try:
        if request.method == "POST":
            status = UpdateStatusForm(request.POST, instance=ticket)
            if status.is_valid():
                status.save()
                return redirect(ticket_details, ticket.pk)
    except Exception as e:
        print(e)
        messages.error(request, "An error has occurred and status was not update. Please check log.")
        return redirect(ticket_details, ticket.pk)
