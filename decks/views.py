from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.urls import reverse_lazy
from common.stats_services import get_annotated_decks
from .models import Deck


# Deck Creation View
class DeckCreateView(CreateView):
    model = Deck
    # Only set commander and description, the rest is auto
    fields = ("commander_name", "description")
    template_name = "deck_form.html"
    context_object_name = "deck"

    def get_success_url(self):
        # Redirect to owned decks page with new deck
        return reverse_lazy("all_owned_decks", kwargs={"pk": self.request.user.pk})

    def form_valid(self, form):
        # Automatically set owner to active user
        form.instance.created_by = self.request.user
        return super().form_valid(form)


# A list view for all system decks
class DeckListView(LoginRequiredMixin, ListView):
    model = Deck
    template_name = "deck_list.html"
    paginate_by = 10  # Paginate the results
    context_object_name = "deck_list"


# A list view that filters decks for a specific user (current implementation is active user)
class UserDeckListview(LoginRequiredMixin, ListView):
    model = Deck
    template_name = "deck_list.html"  # Use the same template as other deck list view
    paginate_by = 10
    context_object_name = "deck_list"

    def get_queryset(self):  # Filter the queryset down to owned decks
        return Deck.objects.filter(created_by__pk=self.kwargs["pk"])


# Detail view for more in depth deck data.
class DeckDetailView(LoginRequiredMixin, DetailView):
    model = Deck
    template_name = "deck_detail.html"
    context_object_name = "deck"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get deck specific stats (num games, wins, winrate)
        deck = self.object
        deck = get_annotated_decks().filter(pk=deck.pk).first

        context["deck_stats"] = deck
        return context


# Deck Update View (with user auth)
class DeckUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Deck
    fields = ("commander_name", "description", "active")
    template_name = "deck_form.html"  # Reuse deck creation template
    context_object_name = "deck"

    def get_success_url(self):
        # Redirect to owned decks page with new deck
        return reverse_lazy("all_owned_decks", kwargs={"pk": self.request.user.pk})

    # Test to ensure users can only edit their own decks
    def test_func(self):
        deck = self.get_object()
        return deck.created_by == self.request.user


# Deck Delete View (with user auth)
class DeckDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Deck
    template_name = "deck_delete.html"

    # Redirect to owned decks page
    def get_success_url(self):
        return reverse_lazy("all_owned_decks", kwargs={"pk": self.request.user.pk})

    # Test to ensure users can only edit their own decks
    def test_func(self):
        deck = self.get_object()
        return deck.created_by == self.request.user
