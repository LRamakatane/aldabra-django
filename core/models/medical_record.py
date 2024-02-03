"""Medical Record"""

from django.db import models
from core.models.defaults import default_encounter, default_medical_history
import uuid
from core.models.validators.medical_record import (
    validate_encounters,
    validate_medical_history,
)


class Allergy(models.Model):
    pass


class MedicalRecord(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, unique=True)
    patient = models.OneToOneField("Patient", on_delete=models.DO_NOTHING, null=True)
    encounters = models.JSONField(
        default=default_encounter,
        blank=True,
        null=True,
        serialize=True,
        validators=[validate_encounters],
    )
    allergies = models.ManyToManyField("Allergy", blank=True)
    medical_history = models.JSONField(
        default=default_medical_history,
        blank=True,
        null=True,
        serialize=True,
        validators=[validate_medical_history],
    )

    def __str__(self) -> str:
        return f"{self.patient}"
