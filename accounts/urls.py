from django.urls import path
from .views import ProfileSignupView, ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path("signup/", ProfileSignupView.as_view(), name="signup"),
    path("<int:pk>/", ProfileDetailView.as_view(), name="profile_detail"),
    path("<int:pk>/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
]
