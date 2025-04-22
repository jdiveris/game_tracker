from django.db import models


class Game(models.Model):
    date = models.DateField()
    winner = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.SET_NULL,
        related_name="games_won",
        null=True,
    )
    turn_1 = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.SET_NULL,
        related_name="games_started",
        null=True,
    )
    first_elim = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.SET_NULL,
        related_name="games_first_out",
        null=True,
    )
    win_condition = models.CharField(max_length=70)
    notes = models.TextField(max_length=280)
    draw = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} {self.id}"


class PlayerGame(models.Model):
    class MulliganCount(models.IntegerChoices):
        NONE = 7, "None"
        ONE = 6, "Mull to 6"
        TWO = 5, "Mull to 5"
        THREE = 4, "Mull to 4"
        FOUR = 3, "Mull to 3"
        FIVE = 2, "Mull to 2"

    player = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.SET_NULL,
        related_name="games_played_in",
        null=True,
    )
    game = models.ForeignKey(
        "Game", on_delete=models.CASCADE, related_name="player_games"
    )
    deck = models.ForeignKey(
        "decks.Deck",
        on_delete=models.SET_NULL,
        related_name="decks_in_this_game",
        null=True,
    )
    mulligan = models.IntegerField(
        choices=MulliganCount.choices,
        default=MulliganCount.NONE,
    )
    concede = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.player.display_name} in Game {self.game}"
