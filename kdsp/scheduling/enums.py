from kdsp.common.enums import BaseEnum


class AppointmentTypes(BaseEnum):
    OT = ("OT", "Occupational")
    PT = ("PT", "Physical")
    ST = ("ST", "Speech")


class AppointmentStatuses(BaseEnum):
    PENDING_DETAILS = ("PENDING DETAILS", "Pending Details")
    PENDING_PAYMENT = ("PENDING PAYMENT", "Pending Payment")
    PENDING_APPROVAL = ("PENDING APPROVAL", "Pending Approval")
    SCHEDULED = ("SCHEDULED", "Scheduled")
    CANCELLED = ("CANCELLED", "Cancelled")
    COMPLETED = ("COMPLETED", "Completed")


class PatientAppointmentFilterKeys(BaseEnum):
    UPCOMING = ("UPCOMING", "upcoming")
    PREVIOUS = ("PREVIOUS", "previous")


class TherapistAppointmentFilterKeys(BaseEnum):
    WAITING = ("WAITING", "waiting")
    PENDING_APPROVAL = ("PENDING_APPROVAL", "pending-approval")
    SCHEDULED = ("SCHEDULED", "scheduled")
    PREVIOUS = ("PREVIOUS", "previous")


class WeekDays(BaseEnum):
    MONDAY = ("MONDAY", "Monday")
    TUESDAY = ("TUESDAY", "Tuesday")
    WEDNESDAY = ("WEDNESDAY", "Wednesday")
    THURSDAY = ("THURSDAY", "Thursday")
    FRIDAY = ("FRIDAY", "Friday")
    SATURDAY = ("SATURDAY", "Saturday")
    SUNDAY = ("SUNDAY", "Sunday")

