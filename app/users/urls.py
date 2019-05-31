from . import views

from django.contrib.auth import views as auth_views
from django.urls import path


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("", views.index, name="index"),
]

