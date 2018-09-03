from django.urls import path
from .views import *

urlpatterns = [
    path('', issuetrackerhome, name="issuetrackerhome"),
]
