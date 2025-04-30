from django.urls import path
from .views import (
    GameListView,
    GameCreateView,
    GameUpdateView,
    GameDetailView,
    GameDeleteView,
)

urlpatterns = [
    path("list/", GameListView.as_view(), name="all_games"),
    path("new/", GameCreateView.as_view(), name="game_create"),
    path("<int:pk>/", GameDetailView.as_view(), name="game_detail"),
    path("<int:pk>/edit/", GameUpdateView.as_view(), name="game_update"),
    path("<int:pk>/delete/", GameDeleteView.as_view(), name="game_delete"),
]
