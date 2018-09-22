from django.urls import path
from .views import *

urlpatterns = [
    path('', issue_tracker_home, name="issue_tracker_home"),
    path('ticket_ranking_progress/', ticket_ranking_progress, name="ticket_ranking_progress"),
    path('ticket/new/', submit_new_ticket, name="submit_new_ticket"),
    path('ticket/<int:pk>/', ticket_details, name="ticket_details"),
    path('ticket/<int:pk>/edit/', edit_ticket, name="edit_ticket"),
    path('ticket/<int:ticketpk>/comment/<int:commentpk>/edit/', edit_comment, name="edit_comment"),
    path('ticket/<int:pk>/upvote/', upvote, name="upvote"),
    path('ticket/<int:pk>/fund/', fund, name="fund"),
    path('ticket/<int:pk>/update_status/', update_status, name="update_status"),
    path('ticket/<int:pk>/update_threshold/', update_threshold, name="update_threshold"),
]
