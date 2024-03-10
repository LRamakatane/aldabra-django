#!/usr/bin/env python3
"""Doctor"""
from django.db import models
from core.models.defaults import default_name
import uuid


class Doctor(models.Model):
    id = models.UUIDField(
        "User ID", primary_key=True, default=uuid.uuid4, unique=True
    )
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    name = models.JSONField(serialize=True, default=default_name)
    specialization = models.ForeignKey("Specialization",
                                       on_delete=models.DO_NOTHING, blank=True)
    resident_hospital = models.OneToOneField("Hospital",
                                             on_delete=models.DO_NOTHING,
                                             null=True, blank=True, related_name="resident_hospital")
    hospitals = models.ManyToManyField("Hospital", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        title = self.name.get("title", "")
        first = self.name.get("first_name", "")
        last = self.name.get("last_name", "")

        return f"{title} {first} {last}"


class Specialization(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f"{self.name}"
