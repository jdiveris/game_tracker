from django import forms
from .models import Game, PlayerGame
from decks.models import Deck
from accounts.models import Profile


# Form for PlayerGame entries (specific players, decks in a game)
class PlayerGameForm(forms.ModelForm):
    class Meta:
        model = PlayerGame
        fields = ("player", "deck", "mulligan", "concede")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create custom dropdown options
        self.fields["deck"].queryset = (
            # Get all active decks, ordered alphabetically by owner and commander
            Deck.objects.filter(active=True).order_by("created_by", "commander_name")
        )
        self.fields["player"].queryset = (
            # Get all non-admin profiles (players) sorted by display_name
            Profile.objects.filter(is_staff=False).order_by("display_name")
        )


# Custom formset that allows inline creation of PlayerGames with an associated Game
PlayerGameFormSet = forms.inlineformset_factory(
    Game,
    PlayerGame,
    form=PlayerGameForm,
    extra=4,
    can_delete=False,
)
