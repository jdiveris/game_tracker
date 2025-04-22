from django.contrib import admin
from .models import Deck


class DeckAdmin(admin.ModelAdmin):
    list_display = [
        "commander_name",
        "created_by",
        "date_added",
        "date_updated",
        "description",
    ]
    readonly_fields = ("date_added", "date_updated")

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields + ("created_by",)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user.profile
        return super().save_model(request, obj, form, change)


admin.site.register(Deck, DeckAdmin)
