from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.core import cache
from .models import Game
from .forms import PlayerGameFormSet


class GameListView(LoginRequiredMixin, ListView):
    model = Game
    template_name = "games_list.html"
    context_object_name = "games"
    paginate_by = 10


class GameDetailView(LoginRequiredMixin, DetailView):
    model = Game
    template_name = "game_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()
        # Get players and decks associated with this game from db
        players = game.player_games.select_related("player", "deck")
        # Add those players to the context
        context["players_in_game"] = players

        return context


class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    fields = [
        "date",
        "winner",
        "turn_1",
        "first_elim",
        "win_condition",
        "notes",
        "draw",
    ]
    template_name = "game_form.html"

    def get_context_data(self, **kwargs):
        # Get context obj
        context = super().get_context_data(**kwargs)
        # Set Template page title to Create Game
        context["page_title"] = "Create Game"

        if self.request.POST:  # If completed form is being posted
            context["playergame_formset"] = PlayerGameFormSet(self.request.POST)
        else:  # If new form is being accessed
            context["playergame_formset"] = PlayerGameFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        # Access the playergame forms
        playergame_formset = context["playergame_formset"]

        if playergame_formset.is_valid():
            game = form.save(commit=False)  # Get game record without committing to db
            game.recorded_by = self.request.user  # Note who created this game
            game.save()  # Commit game
            playergame_formset.instance = game  # Link playergames and game
            playergame_formset.save()  # Save playergames

            # Reset cached data
            cache.delete("recent_games")
            cache.delete("most_played_decks")
            cache.delete("player_leaderboard")
            cache.delete("deck_leaderboard")

            success_url = reverse_lazy("all_games")  # Redirect to games/list
        else:
            return self.form_invalid(form)


class GameUpdateView(LoginRequiredMixin, UpdateView):
    model = Game
    fields = [
        "date",
        "winner",
        "turn_1",
        "first_elim",
        "win_condition",
        "notes",
        "draw",
    ]
    template_name = "game_form.html"  # Use same form template as create

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Set template page title to Edit Game
        context["page_title"] = "Edit Game"

        if self.request.POST:  # If completed form being submitted
            context["playergame_formset"] = PlayerGameFormSet(
                self.request.POST, instance=self.object
            )
        else:  # If existing game is being accessed and form generated
            context["playergame_formset"] = PlayerGameFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        # Access the playergame forms
        playergame_formset = context["playergame_formset"]

        if playergame_formset.is_valid():
            self.object.recorded_by = self.request.user  # Note who edited this game
            self.object = form.save()  # Save game and set as self.obj
            playergame_formset.instance = self.object  # Link playergames and game
            playergame_formset.save()  # Save playergames

            # Reset cached data
            cache.delete("recent_games")
            cache.delete("most_played_decks")
            cache.delete("player_leaderboard")
            cache.delete("deck_leaderboard")

            success_url = reverse_lazy("all_games")  # Redirect to games/list
        else:
            return self.form_invalid(form)


class GameDeleteView(LoginRequiredMixin, DeleteView):
    model = Game
    template_name = "game_delete.html"
    success_url = reverse_lazy("all_games")
