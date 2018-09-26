from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Count, Sum
from django.db.models.functions import ExtractWeek, ExtractMonth, ExtractYear
from .models import Ticket, Comment, Fund, ProgressLog
from .forms import TicketSubmitForm, CommentPostForm, FundingForm, UpdateStatusForm, UpdateThresholdForm, CardDetailForm
from .filters import TicketFilter
import stripe
import json
import datetime

stripe.api_key = settings.STRIPE_SECRET

# Create your views here.
def issue_tracker_home(request):
    """
    A view that displays the home page of issue tracker.
    """

    tickets = Ticket.objects.all().order_by('-submission_date')
    filter = TicketFilter(request.GET, queryset=tickets)
    paginator = Paginator(filter.qs, 20)
    page = request.GET.get('page')
    tickets = paginator.get_page(page)

    return render(request, "issuetrackerhome.html", {'tickets': tickets, 'filter': filter})

def ticket_ranking_progress(request):
    """
    A view that displays all data visualizations regarding issue tracker.
    """

    today = datetime.datetime.today()

    bug_ranking = Ticket.objects.filter(type="T1") \
        .annotate(upvote_count=Count('upvote_user')) \
        .order_by('-upvote_count') \
        [:5]

    feature_request_ranking = Ticket.objects.filter(type="T2").order_by('-upvote_fund')[:5]

    progress_log = ProgressLog.objects.all()
    pl_daily_filter = ProgressLog.objects.filter(
        date__range=(today-datetime.timedelta(days=6), today)
    ).order_by('date')
    pl_weekly_filter = ProgressLog.objects \
        .filter(date__year=today.year) \
        .filter(date__month=today.month) \
        .annotate(year=ExtractYear('date'), week=ExtractWeek('date')) \
        .values('year', 'week') \
        .annotate(week_bug_total=Sum('bug_tended')) \
        .annotate(week_feature_total=Sum('feature_tended')) \
        .order_by('week')
    pl_monthly_filter = ProgressLog.objects \
        .filter(date__year=today.year) \
        .annotate(year=ExtractYear('date'), month=ExtractMonth('date')) \
        .values('year', 'month') \
        .annotate(month_bug_total=Sum('bug_tended')) \
        .annotate(month_feature_total=Sum('feature_tended')) \
        .order_by('month')

    return render(
        request,
        "ticketrankingprogress.html",
        {
            'bug_ranking': bug_ranking,
            'feature_request_ranking': feature_request_ranking,
            'progress_log': progress_log,
            'pl_daily_filter': pl_daily_filter,
            'pl_weekly_filter': pl_weekly_filter,
            'pl_monthly_filter': pl_monthly_filter,
        })

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

    if ticket.type == "T1" and ticket.status == ("S1" or "S5"):
        if ticket.threshold == None:
            messages.warning(request, "Threshold level has not been set for this ticket yet.")
        elif ticket.upvote_user.count() >= ticket.threshold:
            messages.info(request, "Thank you for your attention, we will begin looking into fixing this bug.")
            ticket.status = "S2"
            ticket.save()
    elif ticket.type == "T2" and ticket.status == ("S1" or "S5"):
        if ticket.threshold == None:
            messages.warning(request, "Threshold level has not been set for this ticket yet.")
        elif ticket.upvote_fund >= ticket.threshold:
            messages.info(request, "Thank you for the funding, we will begin looking into developing this new feature.")
            ticket.status = "S2"
            ticket.save()

    status = UpdateStatusForm(instance=ticket)
    threshold = UpdateThresholdForm(instance=ticket)
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
            'threshold': threshold,
        })

@login_required
def edit_ticket(request, pk):
    """
    A view that allows users to edit existing tickets
    """

    ticket = get_object_or_404(Ticket, pk=pk)

    if request.user == ticket.author:
        if request.method == "POST":
            form = TicketSubmitForm(request.POST, instance=ticket)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.last_modified = timezone.now()
                ticket.save()
                return redirect(ticket_details, ticket.pk)
        else:
            form = TicketSubmitForm(instance=ticket)
    else:
        messages.warning(request, "You are not the author of this ticket and thus not allowed to edit.")
        return redirect(ticket_details, ticket.pk)
    return render(request, 'ticketeditform.html', {'form': form, 'ticket': ticket})

@login_required
def edit_comment(request, ticketpk, commentpk):
    """
    A view that allows user to edit comment they posted
    on a particular ticket.
    """

    ticket = get_object_or_404(Ticket, pk=ticketpk)
    comment = get_object_or_404(Comment, pk=commentpk)
    ticketcomments = Comment.objects.filter(ticket=ticket)

    if comment in ticketcomments:
        if comment.author == request.user:
            if request.method == "POST":
                form = CommentPostForm(request.POST, instance=comment)
                if form.is_valid():
                    form.save()
                    return redirect(ticket_details, ticket.pk)
            else:
                form = CommentPostForm(instance=comment)
        else:
            messages.warning(request, "You are not the author of the comment and thus not allowed to edit.")
            return redirect(ticket_details, ticket.pk)
    else:
        messages.warning(request, "Comment retrieved is not part of this ticket, please check your url.")
        return redirect(ticket_details, ticket.pk)

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
    A view that displays a form for paying towards a feature request ticket, while
    also handling the payment process using Stripe API.
    """

    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method=="POST":
        funding_form = FundingForm(request.POST)
        card_detail_form = CardDetailForm(request.POST)

        if funding_form.is_valid() and card_detail_form.is_valid():
            try:
                donor = stripe.Charge.create(
                    amount = int(funding_form.cleaned_data['fund'] * 100),
                    currency = "GBP",
                    description = "{0} donation on {1}".format(request.user.email, ticket.title),
                    card = card_detail_form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                messages.warning(request, "Your card was declined!")

            if donor.paid:
                messages.success(request, "Thank you for your donation!")
                fund = funding_form.save(commit=False)
                fund.date = timezone.now()
                fund.save()

                ticket.upvote_fund = ticket.upvote_fund + funding_form.cleaned_data['fund']
                ticket.save()

                return redirect(ticket_details, ticket.pk)
            else:
                messages.warning(request, "Unable to take payment.")
        else:
            print(funding_form.errors)
            print(card_detail_form.errors)
            messages.warning(request, "We were not able to take payment from the card you provided.")
            messages.warning(request, funding_form.errors)
    else:
        funding_form = FundingForm(initial={'user': request.user, 'ticket': ticket})
        card_detail_form = CardDetailForm()

    return render(
        request,
        'ticketfundingform.html',
        {
            'ticket': ticket,
            'funding_form': funding_form,
            'card_detail_form': card_detail_form,
            'publishable': settings.STRIPE_PUBLISHABLE,
        })

@staff_member_required
def update_status(request, pk):
    """
    A functional view that allows staff to update status of a ticket from the ticket details view.
    """

    ticket = get_object_or_404(Ticket, pk=pk)

    try:
        if request.method == "POST":
            status = UpdateStatusForm(request.POST, instance=ticket)
            if status.is_valid():
                status.save()
                messages.success(request, "Status has been successfully updated!")
        return redirect(ticket_details, ticket.pk)
    except Exception as e:
        print(e)
        messages.warning(request, "An error has occurred and status was not updated. Please check log.")
        return redirect(ticket_details, ticket.pk)

@staff_member_required
def update_threshold(request, pk):
    """
    A functional view that allows staff to change threshold level of a ticket.
    """

    ticket = get_object_or_404(Ticket, pk=pk)

    try:
        if request.method == "POST":
            threshold = UpdateThresholdForm(request.POST, instance=ticket)
            if threshold.is_valid():
                threshold.save()
                messages.success(request, "Threshold has been successfully updated!")
        return redirect(ticket_details, ticket.pk)
    except Exception as e:
        print(e)
        messages.warning(request, "An error has occurred and threshold was not updated. Please check log.")
        return redirect(ticket_details, ticket.pk)
