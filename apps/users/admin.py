from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.users.forms import UserChangeForm, UserCreationForm

from .models import Address, Profile

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("password",)}),
        (
            _("Personal info"),
            {
                "fields": (
                    "username",
                    "email",
                    "roles",
                    "account_type",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "deleted",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at")}),
    )
    readonly_fields = (
        "last_login",
        "created_at",
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

    list_display = ["username", "email", "account_type", "role", "is_superuser"]
    list_display_links = ["username", "email"]
    search_fields = ["username", "role", "email", "account_type", "id"]
    ordering = ("email",)


admin.site.register(Profile)
admin.site.register(Address)
