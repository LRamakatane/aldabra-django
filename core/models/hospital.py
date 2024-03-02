#!/usr/bin/env python3
"""Hospital"""
import uuid
from django.db import models
from core.models.defaults import default_contact, default_location_data


class Hospital(models.Model):

    HOSPITAL_TYPES = [
        ("SP", "Specialized"),
        ("CL", "Clinic"),
        ("GN", "General"),
        ("LB", "Laboratory")
    ]

    owner = models.OneToOneField("User", on_delete=models.PROTECT)
    id = models.UUIDField(
        "Hospital ID", primary_key=True, default=uuid.uuid4, unique=True
    )
    name = models.CharField(max_length=500)
    contact = models.JSONField(
        default=default_contact, serialize=True, blank=True, null=True
    )
    type = models.CharField(max_length=2, choices=HOSPITAL_TYPES)
    location = models.JSONField(serialize=True, blank=True, default=default_location_data)

    def __str__(self) -> str:
        return f"{self.name}"
