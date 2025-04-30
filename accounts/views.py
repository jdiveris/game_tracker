from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from .forms import ProfileCreationForm
from .models import Profile


class ProfileSignupView(CreateView):
    form_class = ProfileCreationForm
    success_url = reverse_lazy("login")
    template_name = "./templates/registration/signup.html"


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profile_detail.html"
    context_object_name = "profile"


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ("username", "display_name", "bio")
    template_name = "profile_edit.html"

    def get_success_url(self):
        return reverse_lazy("profile_detail", kwargs={"pk": self.request.user.pk})
