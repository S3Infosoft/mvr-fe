from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUserCreateForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = get_user_model()
        fields = "email",


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = "email",


class RegisterForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = get_user_model()
        fields = "email", "first_name", "last_name",

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields["first_name"].required = True
