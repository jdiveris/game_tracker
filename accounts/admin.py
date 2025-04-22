from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import ProfileCreationForm, ProfileChangeForm
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"


class ProfileAdmin(UserAdmin):
    inlines = (ProfileInline,)
    add_form = ProfileCreationForm
    form = ProfileChangeForm

    def display_name(self, obj):
        return obj.profile.display_name

    list_display = [
        "username",
        "email",
        "display_name",
    ]


admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)
