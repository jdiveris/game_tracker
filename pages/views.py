from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from common.stats_services import get_annotated_decks, get_annotated_players
from games.models import Game


# Home Page View
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # Get context obj
        context = super().get_context_data(**kwargs)

        # Check cache for query data
        games = cache.get("recent_games")

        if not games:  # If not in cache
            # Get 5 most recent games from database
            games = Game.objects.order_by("-date")[:5]
            cache.set("recent_games", games, 300)  # Cache them for 5 min

        # Check cache for query data
        decks = cache.get("most_played_decks")

        if not decks:  # If not in cache
            # Get 5 most played Decks from database
            decks = get_annotated_decks(self.request.user).order_by("-games_played")[:5]
            cache.set("most_played_decks", decks, 300)

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

        # Attempt to get cached player data
        players = cache.get("player_leaderboard")

        if not players:  # If data is not in the cache
            players = get_annotated_players()  # Get player data from db
            cache.set("player_leaderboard", players, 300)

        # Attempt to get cached deck data
        decks = cache.get("deck_leaderboard")

        if not decks:  # If data is not in the cache
            decks = get_annotated_decks()  # Get deck data from db
            cache.set("decks_leaderboard", decks, 300)

        # Order the display based on sort selection (winrate is default)
        if sort_by == "winrate":
            players = players.order_by("-winrate")
            decks = decks.order_by("-winrate")
        else:
            players = players.order_by("-wins")
            decks = decks.order_by("-wins")

        # Add to context object
        context["player_leaderboard"] = players
        context["decks_leaderboard"] = decks

        return context


# User Stats Page View
class UserStatsPageView(LoginRequiredMixin, TemplateView):
    template_name = "player_stats.html"

    def get_context_data(self, **kwargs):
        # Get context obj
        context = super().get_context_data(**kwargs)
        # Default the display to sort by winrate
        sort_by = self.request.GET.get("sort_by", "winrate")

        # Attempt to get cached player data
        player = cache.get("player_leaderboard")

        if not player:  # If data is not in the cache
            player = get_annotated_players(self.request.user)  # Get player data from db
            cache.set("player_leaderboard", player, 300)

        # Attempt to get cached deck data
        decks = cache.get("deck_leaderboard")

        if not decks:  # If data is not in the cache
            decks = get_annotated_decks(self.request.user)  # Get deck data from db
            cache.set("decks_leaderboard", decks, 300)

        # Order the display based on sort selection (winrate is default)
        if sort_by == "winrate":
            decks = decks.order_by("-winrate")
        else:
            decks = decks.order_by("-wins")

        # Add to context object
        context["player_stats"] = player
        context["decks_stats"] = decks

        return context
