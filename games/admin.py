from django.contrib import admin
from .models import Game, PlayerGame


class GameAdmin(admin.ModelAdmin):
    list_display = ["id", "date", "decks_played"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("decks_in_this_game")

    def decks_played(self, obj):
        return ", ".join(
            f"{player_game.deck.commander_name}"
            for player_game in obj.player_games.all()
        )


admin.site.register(Game, GameAdmin)
admin.site.register(PlayerGame)
