from . import views

from django.contrib.auth import views as auth_views
from django.urls import path, include

password_urls = [
    path("change/done/", auth_views.PasswordChangeDoneView.as_view(),
         name="password_change_done"),
    path("change/", views.PasswordChangeView.as_view(),
         name="password_change"),
    path("reset/done/", auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path("reset/complete/", auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    path("new/<uidb64>/<token>/",
         views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("reset/", views.PasswordResetView.as_view(),
         name="password_reset"),
]

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("password_", include(password_urls)),
    path("", views.index, name="index"),
]
