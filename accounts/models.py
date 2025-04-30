from django.contrib.auth.models import AbstractUser
from django.db import models


# Profile Class, extend Abstract User model for built in functionality
class Profile(AbstractUser):
    display_name = models.CharField(
        max_length=12, blank=True
    )  # Add a custom display name field
    bio = models.TextField(null=True)  # Add a bio field for user customization
