from django.urls import path
from .views import ProfileSignupView

urlpatterns = [
    path("signup/", ProfileSignupView.as_view(), name="signup"),
]
