from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .forms import ProfileCreationForm, ProfileChangeForm
from .models import Profile


# Display User Profiles on the admin panel
class ProfileAdmin(UserAdmin):
    add_form = ProfileCreationForm
    form = ProfileChangeForm
    model = Profile

    list_display = [
        "username",
        "email",
        "display_name",
    ]

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("display_name",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("display_name",)}),)


admin.site.register(get_user_model(), ProfileAdmin)
