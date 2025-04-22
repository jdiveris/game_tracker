from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Profile
from .forms import ProfileCreationForm


class ProfileSignupView(CreateView):
    form_class = ProfileCreationForm
    success_url = reverse_lazy("login")
    template_name = "./templates/registration/signup.html"
