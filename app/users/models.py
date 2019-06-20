from django.db import models
from django.urls import reverse
from django.contrib.auth import base_user, models as auth_models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.core.files.base import ContentFile

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


def save_image(instance, filename):
    user_id = instance.id
    extension = filename.rsplit(".", 1)[-1]
    timestamp = str(now().date())
    filename = f"{timestamp}.{extension}"
    return "/".join(("profile", str(user_id), filename))


def save_thumb(instance, filename):
    user_id = instance.id
    timestamp = str(now().date())
    extension = filename.rsplit(".", 1)[-1]
    filename = f"{timestamp}.{extension}"
    return "/".join(("profile", str(user_id), "thumb", filename))


class CustomUser(auth_models.AbstractUser):
    """
    CustomUser model with email and password for authentication
    """
    username = None
    email = models.EmailField(_("email address"), unique=True)
    image = models.ImageField(upload_to=save_image, blank=True, null=True)
    image_thumb = models.ImageField(upload_to=save_thumb,
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

    def save(self, *args, **kwargs):
        created = self._state.adding        # created or updated

        if not created:

            # Store the current image in image
            image = self.image
            if image:
                image_name = image.name.rsplit("/", 1)[-1]

                # Create a new image for thumbnail
                thumb_image = ContentFile(image.read())

                # Save the thumbnail but do not commit to the database
                self.image_thumb.save(image_name, thumb_image, False)

                # Save the model
                super(CustomUser, self).save(*args, **kwargs)

                # Get the thumbnail image from its path to resize it
                thumb_image = Image.open(self.image.path)

                if thumb_image.height > 140 or thumb_image.height > 140:
                    output_size = (140, 140)
                    thumb_image.thumbnail(output_size)

                    # Save the resized image to its path
                    thumb_image.save(self.image_thumb.path)
        else:
            super(CustomUser, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the user image or anything after object is deleted

        if self.image:
            self.image.delete(False)
            self.image_thumb.delete(False)
        super(CustomUser, self).delete(*args, **kwargs)
