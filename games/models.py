from django.db import models


class Game(models.Model):
    date = models.DateField()
    recorded_by = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.SET_NULL,
        null=True,
    )
    winner = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.SET_NULL,
        related_name="games_won",
        null=True,
        blank=True,
        verbose_name="Winner",
    )
    turn_1 = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.SET_NULL,
        related_name="games_started",
        null=True,
        blank=True,
        verbose_name="Went First",
    )
    first_elim = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.SET_NULL,
        related_name="games_first_out",
        null=True,
        blank=True,
        verbose_name="First Out",
    )
    win_condition = models.CharField(
        max_length=70,
        null=True,
        blank=True,
        verbose_name="Win Condition",
    )
    notes = models.TextField(max_length=280)
    draw = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name="Draw",
    )

    def __str__(self):
        return f"{self.date} {self.id}"

    @property
    def winning_deck(self):
        if self.winner:
            # Try to find the PlayerGame object where the player == winner
            pg = self.player_games.filter(player=self.winner).first()
            if pg:
                return pg.deck
        return None


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
        related_name="player",
        null=True,
    )
    game = models.ForeignKey(
        "Game",
        on_delete=models.CASCADE,
        related_name="player_games",
    )
    deck = models.ForeignKey(
        "decks.Deck",
        on_delete=models.SET_NULL,
        related_name="deck",
        null=True,
    )
    mulligan = models.IntegerField(
        choices=MulliganCount.choices,
        default=MulliganCount.NONE,
    )
    concede = models.BooleanField(
        default=False,
        verbose_name="Concession",
    )

    def __str__(self):
        return f"{self.player.display_name} in Game {self.game}"
