from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from core.models import Doctor

from services.doctors.api.v1.serializers import DoctorSerializer

from services.utils import Cache, format_response_data
from services.exceptions import exception_handler, handle_error_response

cache = Cache()


class DoctorAPIView(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DoctorSerializer

    def create(self, request, *args, **kwargs):
        try:
            doctor = super().create(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(error, "error occurred while creating doctor")
            return handle_error_response(response, error)

        data = format_response_data(doctor.data, 201, "doctor created")

        cache.invalidate("doctors")
        return Response(data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        try:
            doctor = super().retrieve(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(doctor.data, 200)

        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            doctor = super().update(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(doctor.data, 200)

        cache.invalidate("doctors")
        return Response(data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        try:
            doctors = super().list(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(doctors.data, 200)

        cache.set("doctors", data)
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            doctor = super().destroy(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(doctor.data, 204)

        cache.invalidate("doctors")
        return Response(data, status=status.HTTP_204_NO_CONTENT)
