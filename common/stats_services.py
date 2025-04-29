from accounts.models import Profile
from games.models import Game
from decks.models import Deck
from django.db.models.functions import NullIf
from django.db.models import (
    Case,
    When,
    IntegerField,
    Count,
    F,
    FloatField,
    ExpressionWrapper,
)


def get_annotated_players(player_filter=None):
    # Get all Player objs
    qs = Profile.objects.filter(is_staff=False)

    if player_filter:  # If player filter is set
        # Filter for specific player
        qs = qs.filter(pk=player_filter.pk)

    return qs.annotate(
        # Add field for # of wins
        wins=Count("games_won", distinct=True),
        # Add field for # of games
        games_played=Count("player_games", distinct=True),
        # Add field for win rate
        winrate=ExpressionWrapper(
            F("wins") * 1.0 / NullIf(F("games_played"), 0),
            output_field=FloatField(),
        ),
    )


def get_annotated_decks(player_filter=None):
    # Get all Deck objs
    qs = Deck.objects.filter(active=True)

    if player_filter:  # If player filter is set
        # Only get decks played by this player
        qs = qs.filter(player_games__player=player_filter)

    return qs.annotate(
        # Add field for # of wins
        wins=Count(
            Case(
                When(  # Only count decks that were played by winning player
                    player_games__player=F("player_games__game__winner"),
                    then=1,
                ),
                output_field=IntegerField(),
            ),
            distinct=True,
        ),
        # Add field for # of games
        games_played=Count("player_games", distinct=True),
        # Add field for win rate
        winrate=ExpressionWrapper(
            F("wins") * 1.0 / NullIf(F("games_played"), 0),
            output_field=FloatField(),
        ),
    )
