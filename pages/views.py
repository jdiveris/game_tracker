from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from common.stats_services import get_annotated_decks, get_annotated_players
from games.models import Game


# Home Page View
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # Get context obj
        context = super().get_context_data(**kwargs)

        # Get 5 most recent games from database
        games = Game.objects.order_by("-date")[:5]

        # Get 5 most played Decks from database
        decks = get_annotated_decks(self.request.user).order_by("-games_played")[:5]

        # Add to context object
        context["recent_games"] = games
        context["most_played_decks"] = decks

        return context


# Stats Page View
class StatsPageView(LoginRequiredMixin, TemplateView):
    template_name = "leaderboard.html"

    def get_context_data(self, **kwargs):
        # Get context obj
        context = super().get_context_data(**kwargs)
        # Default the display to sort by winrate
        sort_by = self.request.GET.get("sort_by", "winrate")

        players = get_annotated_players()  # Get player data from db

        decks = get_annotated_decks()  # Get deck data from db

        # Order the display based on sort selection (winrate is default)
        if sort_by == "winrate":
            players = players.order_by("-winrate")
            decks = decks.order_by("-winrate")
        else:
            players = players.order_by("-wins")
            decks = decks.order_by("-wins")

        # Add to context object
        context["player_leaderboard"] = players
        context["deck_leaderboard"] = decks

        return context


# User Stats Page View
class UserStatsPageView(LoginRequiredMixin, TemplateView):
    template_name = "player_stats.html"

    def get_context_data(self, **kwargs):
        # Get context obj
        context = super().get_context_data(**kwargs)
        # Default the display to sort by winrate
        sort_by = self.request.GET.get("sort_by", "winrate")

        # Get player data from db
        player = get_annotated_players(self.request.user).first()

        # Get deck data from db
        decks = get_annotated_decks(self.request.user)

        # Order the display based on sort selection (winrate is default)
        if sort_by == "winrate":
            decks = decks.order_by("-winrate")
        else:
            decks = decks.order_by("-wins")

        # Add to context object
        context["player_stats"] = player
        context["decks_stats"] = decks

        return context
