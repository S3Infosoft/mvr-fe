from .forms import RegisterForm

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import views, decorators, get_user_model, mixins
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.http import urlsafe_base64_decode

import logging

logger = logging.getLogger("auth")


class ProfileDetailUpdate(mixins.LoginRequiredMixin,
                          SuccessMessageMixin,
                          generic.UpdateView):
    model = get_user_model()
    fields = "email", "first_name", "last_name",
    template_name = "users/profile.html"
    success_message = "Your profile has been successfully updated."

    def get_object(self, queryset=None):

        return self.request.user

    def form_valid(self, form):
        logger.info("Profile Updated by {}".format(self.request.user.email))
        return super(ProfileDetailUpdate, self).form_valid(form)


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
            return redirect("index")

        return super(LoginView, self).get(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.cleaned_data["username"]
        logger.info("LOGIN by {}".format(user))
        return super(LoginView, self).form_valid(form)


class RegisterView(SuccessMessageMixin, generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "users/register.html"
    success_message = "You have been successfully registered," \
                      " login with your email and password."

    def get(self, request, *args, **kwargs):

        # Prevent already logged in user from this page
        if self.request.user.is_authenticated:
            return redirect("index")
        
        return super(RegisterView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        logger.info("REGISTRATION by {}".format(email))
        return super(RegisterView, self).form_valid(form)


class PasswordChangeView(SuccessMessageMixin, views.PasswordChangeView):
    success_message = "Your password has been successfully changed."
    success_url = reverse_lazy("profile")
    
    def form_valid(self, form):
        email = self.request.user.email
        logger.info("PASSWORD-CHANGE by {}".format(email))
        return super(PasswordChangeView, self).form_valid(form)


class PasswordResetView(views.PasswordResetView):

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        logger.info("PASSWORD-RESET request for {}".format(email))
        return super(PasswordResetView, self).form_valid(form)


class PasswordResetConfirmView(SuccessMessageMixin,
                               views.PasswordResetConfirmView):
    success_message = "Your new password has been set," \
                      " login with email and new password."

    def form_valid(self, form):
        user_id = urlsafe_base64_decode(self.kwargs.get("uidb64"))
        user = get_object_or_404(get_user_model(), id=user_id)
        logger.info("PASSWORD-RESET by {}".format(user))
        return super(PasswordResetConfirmView, self).form_valid(form)
    
    def form_invalid(self, form):
        print("Entered invalid")
        return super(PasswordResetConfirmView, self).form_invalid(form)
