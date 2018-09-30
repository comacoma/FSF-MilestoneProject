from django.urls import path
from .views import *

urlpatterns = [
    path('', blog_home, name="blog_home"),
    path('myblogs/', user_blog_home, name="user_blog_home"),
    path('new/', create_or_edit_post, name="new_post"),
    path('<int:pk>/', post_detail, name="post_detail"),
    path('<int:pk>/edit/', create_or_edit_post, name="edit_post"),
]
