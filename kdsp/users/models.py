from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from kdsp.mixins import CreateUpdateMixin


class User(AbstractUser):
    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return f"{self.id} | {self.first_name}"


class Speciality(CreateUpdateMixin):
    name = models.CharField("Name", max_length=50)
    code = models.CharField("Short Code", max_length=6)
    is_active = models.BooleanField("Active", default=True)
    fees = models.IntegerField("Fees", default=0)

    def __str__(self):
        return f"{self.name} {self.code}"

    class Meta:
        verbose_name_plural = "Specialities"


class Patient(models.Model):
    name = models.CharField("Name", max_length=100)
    age = models.FloatField(
        "Age", default=0, validators=[MaxValueValidator(6.5), MinValueValidator(0)]
    )
    parent_name = models.CharField("Parent Name", max_length=100)
    contact = PhoneNumberField()
    sessions = models.IntegerField(
        "Therapy Sessions",
        default=1,
        validators=[MaxValueValidator(3), MinValueValidator(1)],
    )


class Therapist(models.Model):
    name = models.CharField("Name", max_length=100)
    contact = PhoneNumberField()
    speciality = models.ForeignKey(
        Speciality, related_name="therapists", on_delete=models.DO_NOTHING
    )
    is_active = models.BooleanField("Active", default=True)
    work_experience = models.IntegerField(
        default=0, validators=[MaxValueValidator(60), MinValueValidator(0)]
    )


class Education(CreateUpdateMixin):
    degree = models.CharField("Education Degree", max_length=100)
    institution = models.CharField("Institution", max_length=100)
    completion_year = models.CharField("Completion Year", max_length=4, blank=True)
    therapist = models.ForeignKey(
        Therapist, related_name="educations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.degree} | {self.institution} | {self.completion_year}"
