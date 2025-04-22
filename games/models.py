from django.db import models


# Create your models here.
class Game(models.Model):
    date = models.DateField()
    winner = models.ForeignKey(
        "Profile",
        on_delete=models.SET_NULL,
        related_name="games_won",
    )
    turn_1 = models.ForeignKey(
        "Profile",
        on_delete=models.SET_NULL,
        related_name="games_started",
    )
    first_elim = models.ForeignKey(
        "Profile",
        on_delete=models.SET_NULL,
        related_name="games_first_out",
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
        "Profile",
        on_delete=models.SET_NULL,
        related_name="games_played_in",
    )
    game = models.ForeignKey(
        "Game",
        on_delete=models.SET_NULL,
        related_name="games_with_this_player",
    )
    deck = models.ForeignKey(
        "decks.Deck",
        on_delete=models.SET_NULL,
        related_name="games_with_this_deck",
    )
    mulligan = models.IntegerField(
        choices=MulliganCount.choices,
        default=MulliganCount.NONE,
    )
    concede = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.player.user.username} in Game {self.game}"
