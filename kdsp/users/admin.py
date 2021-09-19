from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from kdsp.scheduling.admin import AvailabilityConfigInline
from kdsp.users.forms import UserChangeForm, UserCreationForm
from kdsp.users.models import Education, Patient, Speciality, Therapist

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "first_name", "last_name", "is_superuser"]
    search_fields = ["first_name", "last_name"]


class EducationInline(admin.StackedInline):
    model = Education
    extra = 0
    show_change_link = True


class TherapistAdmin(admin.ModelAdmin):
    inlines = [EducationInline, AvailabilityConfigInline]
    list_display = ["id", "name", "is_active"]


admin.site.register(Therapist, TherapistAdmin)
admin.site.register(Patient)
admin.site.register(Speciality)
admin.site.register(Education)
