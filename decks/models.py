from django.db import models


# Create your models here.
class Deck(models.Model):
    created_by = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
        related_name="decks_created_by",
    )
    commander_name = models.CharField(max_length=65)
    description = models.CharField(max_length=140)
    date_added = models.DateField(auto_now_add=True, null=False)
    date_updated = models.DateField(auto_now=True, null=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.commander_name} | {self.created_by.display_name}"
