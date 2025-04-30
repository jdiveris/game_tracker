from django.db import models


# Deck model to hold basic info about a given EDH Deck
class Deck(models.Model):
    created_by = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
        related_name="decks_created_by",
        blank=True,
        verbose_name="Owner",
    )
    commander_name = models.CharField(
        max_length=65,
        verbose_name="Commander",
    )
    description = models.CharField(max_length=140)
    date_added = models.DateField(
        auto_now_add=True, null=False
    )  # Auto set date on creation
    date_updated = models.DateField(
        auto_now=True, null=False
    )  # Auto set date on update
    active = models.BooleanField(
        default=True,
        verbose_name="Active Status",  # Set decks as inactive without deleting
    )

    def __str__(self):
        return f"{self.commander_name} | {self.created_by.display_name}"
