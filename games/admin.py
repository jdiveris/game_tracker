from django.contrib import admin
from .models import Game, PlayerGame
from decks.models import Deck
from accounts.models import Profile


# Filter to allow to select for games with a specific player in Admin
class PlayerParticipationFilter(admin.SimpleListFilter):
    title = "Player"
    parameter_name = "player"

    def lookups(self, request, model_admin):
        players = Profile.objects.all()
        return [(p.id, p.display_name or p.username) for p in players]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(player_games__player_id=self.value())
        return queryset


# Filter to allow selection for games with specific decks in Admin
class DeckParticipationFilter(admin.SimpleListFilter):
    title = "Deck Played"
    parameter_name = "deck"

    def lookups(self, request, model_admin):
        decks = Deck.objects.all()
        return [(d.id, d.commander_name) for d in decks]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(player_games__deck_id=self.value())
        return queryset


# An inline Playergame class
class PlayerGameInline(admin.TabularInline):
    model = PlayerGame
    extra = 1


# A parent class to hold the inline Playergame
class GameAdmin(admin.ModelAdmin):
    inlines = [PlayerGameInline]
    list_display = [
        "id",
        "date",
        "winner",
        "decks_played",
    ]
    list_filter = [
        "winner",
        "draw",
        PlayerParticipationFilter,
        DeckParticipationFilter,
    ]

    def get_queryset(self, request):
        # Get decks associated with this game
        return super().get_queryset(request).prefetch_related("player_games__deck")

    def decks_played(self, obj):
        return ", ".join(
            f"{player_game.deck.commander_name}"
            for player_game in obj.player_games.all()
        )

    decks_played.short_description = "Decks"


admin.site.register(Game, GameAdmin)
