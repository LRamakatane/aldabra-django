from rest_framework import serializers
from core.models import Doctor


class DoctorSerializer():
    
    class Meta:
        model = Doctor
        fields = "__all__"