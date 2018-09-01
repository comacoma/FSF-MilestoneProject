from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('register/', registration, name="registration"),
    path('profile/', user_profile, name="profile"),
]
