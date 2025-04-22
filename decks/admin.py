from django.contrib import admin
from .models import Deck


class DeckAdmin(admin.ModelAdmin):
    list_filter = [
        "created_by",
        "active",
    ]
    list_display = [
        "commander_name",
        "created_by",
        "date_added",
        "date_updated",
        "description",
    ]
    readonly_fields = ("date_added", "date_updated")


admin.site.register(Deck, DeckAdmin)
