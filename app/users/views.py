from .forms import RegisterForm

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import views, decorators
from django.views import generic


@decorators.login_required
def index(request):
    return render(request, "index.html")


class LoginView(views.LoginView):
    template_name = "users/login.html"
    success_url = reverse_lazy("index")

    def get(self, request, *args, **kwargs):

        # Prevent already login user from this page
        if self.request.user.is_authenticated:
            return redirect("/")

        return super(LoginView, self).get(request, *args, **kwargs)


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "users/register.html"

    def get(self, request, *args, **kwargs):

        # Prevent already logged in user from this page
        if self.request.user.is_authenticated:
            return redirect("/")
        
        return super(RegisterView, self).get(request, *args, **kwargs)
