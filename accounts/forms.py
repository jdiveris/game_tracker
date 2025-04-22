from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Profile


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
