from django.urls import path
from .views import (
    DeckCreateView,
    DeckDetailView,
    DeckUpdateView,
    DeckDeleteView,
    DeckListView,
    UserDeckListview,
)

urlpatterns = [
    path("new/", DeckCreateView.as_view(), name="new_deck"),
    path("list/", DeckListView.as_view(), name="all_decks"),
    path("lists/<int:pk>/", UserDeckListview.as_view(), name="all_owned_decks"),
    path("<int:pk>/", DeckDetailView.as_view(), name="deck_detail"),
    path("<int:pk>/edit/", DeckUpdateView.as_view(), name="deck_edit"),
    path("<int:pk>/delete/", DeckDeleteView.as_view(), name="deck_delete"),
]
