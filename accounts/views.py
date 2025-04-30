from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from .forms import ProfileCreationForm
from .models import Profile


# Signup class
class ProfileSignupView(CreateView):
    form_class = ProfileCreationForm  # Point to creation form
    success_url = reverse_lazy("login")  # Redirect to login
    template_name = "signup.html"


# Detail view for basic account info
class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profile_detail.html"
    context_object_name = "profile"


# Allow User to customize elements of their profile
class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ("username", "display_name", "bio")
    template_name = "profile_edit.html"

    # Redirect back to Profile page
    def get_success_url(self):
        return reverse_lazy("profile_detail", kwargs={"pk": self.request.user.pk})
