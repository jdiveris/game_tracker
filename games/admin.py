from django.contrib import admin
from .models import Game, PlayerGame


class PlayerGameInline(admin.TabularInline):
    model = PlayerGame
    extra = 1


class GameAdmin(admin.ModelAdmin):
    inlines = [PlayerGameInline]
    list_display = ["id", "date", "winner", "decks_played"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("player_games__deck")

    def decks_played(self, obj):
        return ", ".join(
            f"{player_game.deck.commander_name}"
            for player_game in obj.player_games.all()
        )

    decks_played.short_description = "Decks"


admin.site.register(Game, GameAdmin)
