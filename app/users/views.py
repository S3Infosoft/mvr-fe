from .forms import RegisterForm

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import views, decorators
from django.contrib.messages.views import SuccessMessageMixin


@decorators.login_required
def index(request):
    return render(request, "index.html")


class LoginView(SuccessMessageMixin, views.LoginView):
    template_name = "users/login.html"
    success_url = reverse_lazy("index")
    success_message = "You are successfully logged in."

    def get(self, request, *args, **kwargs):

        # Prevent already login user from this page
        if self.request.user.is_authenticated:
            return redirect("/")

        return super(LoginView, self).get(request, *args, **kwargs)


class RegisterView(SuccessMessageMixin, generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "users/register.html"
    success_message = "You have been successfully registered," \
                      " login with your email and password."

    def get(self, request, *args, **kwargs):

        # Prevent already logged in user from this page
        if self.request.user.is_authenticated:
            return redirect("/")
        
        return super(RegisterView, self).get(request, *args, **kwargs)


class PasswordChangeView(SuccessMessageMixin, views.PasswordChangeView):
    success_message = "Your password has been successfully changed."


class PasswordResetConfirmView(SuccessMessageMixin,
                               views.PasswordResetConfirmView):
    success_message = "Your new password has been set," \
                      " login with email and new password."
