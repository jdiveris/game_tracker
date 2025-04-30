from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Profile


# Profile Creation form (signup) -- used in admin and web page
class ProfileCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "display_name",
        )


# Form for user profile editing -- used in django admin
class ProfileChangeForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "display_name",
        )
