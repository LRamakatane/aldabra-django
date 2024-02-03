#!/usr/bin/env python3
"""Patient"""
from django.db import models
from core.models.defaults import default_name, default_contact
import uuid


class Patient(models.Model):
    id = models.UUIDField("Patient ID", primary_key=True, default=uuid.uuid4,
                          unique=True)
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    name = models.JSONField(serialize=True, default=default_name, blank=True)
    hospitals = models.ManyToManyField("Hospital", blank=True, related_name="hospital")
    primary_hospital = models.OneToOneField("Hospital", blank=True, null=True,
                                            on_delete=models.DO_NOTHING)
    contact = models.JSONField(serialize=True, default=default_contact,
                               blank=True)

    def __str__(self) -> str:
        first = self.name.get("first_name", "")
        last = self.name.get("last_name", "")

        return f"{first} {last}"
