from django.urls import path
from .views import *

urlpatterns = [
    path('', issuetrackerhome, name="issuetrackerhome"),
    path('new-ticket/', submitnewticket, name="submitnewticket"),
]
