from django.urls import path
from .views import HomePageView, StatsPageView, UserStatsPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("stats/", StatsPageView.as_view(), name="stats"),
    path("<int:pk>/stats", UserStatsPageView.as_view(), name="user_stats"),
]
