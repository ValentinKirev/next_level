from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin

from next_level.accounts.forms import UserCreateForm
from next_level.accounts.models import Profile

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(auth_admin.UserAdmin):
    add_form = UserCreateForm
    list_display = ('username', 'email', 'is_superuser', 'is_staff', 'is_active')

    fieldsets = (
        (
            None, {
                "fields": (
                    "username",
                    "email",
                    "password"
                )
            }
        ),
        (
            "Permissions", {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important dates", {
                "fields": (
                    "last_login",
                )
            }
        ),
    )

    add_fieldsets = (
        (
            None, {
                "classes": (
                    "wide",
                ),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
