from django.contrib import admin
from core.models import Hospital, MedicalRecord, Patient, Doctor, User, Role, Specialization

# -- register models on django site admin --
admin.site.register(
    [
        Hospital,
        MedicalRecord,
        Patient,
        Doctor,
        User,
        Role,
        Specialization
    ]
)