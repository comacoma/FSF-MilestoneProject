from django.urls import path
from .views import *

urlpatterns = [
    path('', blog_home, name="blog_home"),
]
