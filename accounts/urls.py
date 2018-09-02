from django.urls import path, include
from .views import *
from django.contrib.auth.views import *

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('register/', registration, name="registration"),
    path('profile/', user_profile, name="profile"),
    path('password/', include([
        path('password_change/', PasswordChangeView.as_view(), name='password_change'),
        path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
        path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
        path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
        path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ])),
]
