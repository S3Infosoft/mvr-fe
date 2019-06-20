from django.db import models
from django.urls import reverse
from django.contrib.auth import base_user, models as auth_models
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import ContentFile

from copy import deepcopy

from PIL import Image


class CustomUserManager(base_user.BaseUserManager):
    """
    CustomUser manager for CustomUser for authentication using email and
    password
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create a user with given email and password
        """

        if email:
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)

            return user

        raise ValueError(_("Email must entered to create a user"))

    def create_superuser(self, email, password, **extra_fields):
        """
        Create a superuser with given email, password and other credentials
        """

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError(_("Superuser must have is_staff=True"))
        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self.create_user(email, password, **extra_fields)


class CustomUser(auth_models.AbstractUser):
    """
    CustomUser model with email and password for authentication
    """
    username = None
    email = models.EmailField(_("email address"), unique=True)
    image = models.ImageField(upload_to="profile_pic/%Y/%m/",
                              blank=True,
                              null=True)
    image_thumb = models.ImageField(upload_to="profile_pic/thumb/%Y/%m/",
                                    blank=True,
                                    null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @staticmethod
    def get_absolute_url():
        return reverse("profile")
