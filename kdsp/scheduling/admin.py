from django.contrib import admin
from kdsp.scheduling.models import (
    Appointment,
    Availability,
    AvailabilityConfig,
    CustomAvailability,
)


class AvailabilityInline(admin.StackedInline):
    model = Availability
    extra = 0
    fields = ("id", "day_of_week", "start_time", "end_time")
    readonly_fields = ("id", "created_at", "last_updated_at")


class AvailabilityConfigInline(admin.StackedInline):
    model = AvailabilityConfig
    extra = 0
    fields = ("id", "recurring")
    readonly_fields = ("id", "created_at", "last_updated_at")
    inlines = [AvailabilityInline]


class AvailabilityConfigAdmin(admin.ModelAdmin):
    inlines = [AvailabilityInline]
    list_display = ["id", "recurring"]


admin.site.register(AvailabilityConfig, AvailabilityConfigAdmin)
admin.site.register(Availability)
admin.site.register(CustomAvailability)

admin.site.register(Appointment)
