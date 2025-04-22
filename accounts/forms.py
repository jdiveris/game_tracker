from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile


class ProfileCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
        )

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            display_name = user.username
            Profile.objects.create(user=user, display_name=display_name)
        return user


class ProfileChangeForm(UserChangeForm):
    class Meta:
        display_name = forms.CharField(max_length=30, required=False)
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
        )

    def save(self, commit=True):
        user = super().save(commit=True)
        if commit and hasattr(user, "profile"):
            new_display_name = self.cleaned_data.get("display_name")
            if new_display_name:
                user.profile.display_name = new_display_name
                user.profile.save()
        return user
