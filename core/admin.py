from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ["username", "email", "role", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("role", "phone_number")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "role", "phone_number"),
            },
        ),
    )

admin.site.register(User, CustomUserAdmin)
