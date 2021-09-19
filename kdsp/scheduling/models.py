from collections import defaultdict
from datetime import date, datetime, timedelta

from django.contrib.postgres.fields import DateRangeField
from django.db import models
from django.db.models import Q

from kdsp.mixins import CreateUpdateMixin
from kdsp.scheduling.enums import (
    AppointmentStatuses,
    AppointmentTypes, WeekDays,
)
from kdsp.users.models import Therapist, Patient


class Appointment(CreateUpdateMixin):
    date = models.DateField("Appointment date", null=True, blank=True)
    time = models.TimeField("Appointment time", null=True, blank=True)
    duration = models.IntegerField(
        "Appointment duration in minutes", null=True, blank=False, default=15
    )
    patient = models.ForeignKey(
        Patient,
        null=False,
        blank=False,
        related_name="patient_appointments",
        on_delete=models.CASCADE,
    )
    therapist = models.ForeignKey(
        Therapist,
        null=False,
        blank=False,
        related_name="therapist_appointments",
        on_delete=models.CASCADE,
    )
    appointment_type = models.CharField(
        "Appointment type",
        max_length=50,
        choices=AppointmentTypes.get_choices(),
        null=False,
        blank=False,
    )
    status = models.CharField(
        "Appointment status",
        max_length=50,
        choices=AppointmentStatuses.get_choices(),
        default=AppointmentStatuses.PENDING_PAYMENT.code,
        null=False,
        blank=False,
    )
    fee = models.DecimalField(
        "Therapist fee",
        max_digits=5,
        decimal_places=2,
        null=False,
        blank=False,
        default=0.0,
    )

    class Meta:
        unique_together = ("date", "time", "patient_id", "therapist_id")


class AvailabilityConfig(CreateUpdateMixin):
    therapist = models.ForeignKey(
        Therapist, on_delete=models.CASCADE, related_name="availability_configs"
    )
    recurring = DateRangeField("Recurring")

    @staticmethod
    def get_config_availabilities(config):
        availabilities = config.availabilities.all()
        data = defaultdict(list)
        # merge and format availabilities by days
        for availability in availabilities:
            data[availability.day_of_week].append(
                {
                    "start_time": availability.start_time,
                    "end_time": availability.end_time,
                    "audio": availability.audio,
                    "video": availability.video,
                }
            )
        return data

    @staticmethod
    def get_slots(ranges, slot_size):
        slots = []
        for range_ in ranges:
            start = datetime.combine(date.today(), range_["start_time"])
            end = datetime.combine(date.today(), range_["end_time"])
            while start < end:
                slots.append(
                    {
                        "slot": start.strftime("%I:%M %p"),
                        "audio": range_["audio"],
                        "video": range_["video"],
                    }
                )
                start += timedelta(minutes=slot_size)
        return slots

    @staticmethod
    def get_custom_ranges(custom_availabilities):
        ranges = []
        for custom_availability in custom_availabilities:
            ranges.append(
                {
                    "start_time": custom_availability.start_time,
                    "end_time": custom_availability.end_time,
                    "audio": custom_availability.audio,
                    "video": custom_availability.video,
                }
            )
        return ranges

    @classmethod
    def get_availabilities(
        cls, therapist_id, lower=None, upper=None, slot_size=15
    ):
        """
        :param therapist_id:
        :param lower: start date and would be current date if not provided
        :param upper: end date and would be current date + 7 date if not provided
        :param slot_size: size of time slot in minutes, default is 15 minutes
        """
        result = []
        lower = lower or date.today()
        upper = upper or lower + timedelta(days=6)
        delta = (upper - lower).days
        # getting all the configs containing all days between lower and upper bound
        configs = cls.objects.filter(
            Q(Q(recurring__contains=lower) | Q(recurring__contains=upper)),
            therapist_id=therapist_id,
        ).prefetch_related("availabilities", "custom_availabilities")
        if not configs:
            return []
        configs = iter(configs)
        config = next(configs)
        # get list of week dates | adding +1 in delta because of range exclusion
        availability_dates = [lower + timedelta(days=i) for i in range(delta + 1)]
        availabilities = cls.get_config_availabilities(config)
        for availability_date in availability_dates:
            if availability_date not in config.recurring:
                # checking if the start dates are not in config then skip the
                # date and continue to the next date
                if not result:
                    continue
                try:
                    config = next(configs)
                except StopIteration:
                    # if there is no config available for any date stops the
                    # process and returns the result
                    return result
                availabilities = cls.get_config_availabilities(config)
            day = availability_date.strftime("%A")
            custom_availabilities = config.custom_availabilities.filter(
                date=availability_date
            )
            # checking if there is a custom availability set for a date
            # skip the availability slots and replace them with custom ones
            if custom_availabilities:
                ranges = cls.get_custom_ranges(custom_availabilities)
                slots = cls.get_slots(ranges, slot_size)
            else:
                slots = cls.get_slots(availabilities[day.upper()], slot_size)
            result.append({availability_date.strftime("%a %b %d %Y"): slots})
        return result

    def __str__(self):
        return f"{self.therapist_id} | {self.recurring}"


class Availability(CreateUpdateMixin):
    config = models.ForeignKey(
        AvailabilityConfig, related_name="availabilities", on_delete=models.CASCADE
    )
    day_of_week = models.CharField(
        "Day",
        choices=WeekDays.get_choices(),
        default=WeekDays.MONDAY.code,
        max_length=10,
    )
    start_time = models.TimeField("Start Time")
    end_time = models.TimeField("End Time")

    class Meta:
        verbose_name_plural = "Availabilities"


class CustomAvailability(CreateUpdateMixin):
    config = models.ForeignKey(
        AvailabilityConfig,
        related_name="custom_availabilities",
        on_delete=models.CASCADE,
    )
    date = models.DateField("Date")
    start_time = models.TimeField("Start Time")
    end_time = models.TimeField("End Time")

    class Meta:
        verbose_name_plural = "Custom Availabilities"
