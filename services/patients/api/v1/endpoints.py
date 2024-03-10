from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from core.models import Patient

from services.patients.api.v1.serializers import PatientSerializer

from services.utils import Cache, format_response_data
from services.exceptions import exception_handler, handle_error_response

cache = Cache()


class PatientAPIView(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('-created_at')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PatientSerializer

    def create(self, request, *args, **kwargs):
        try:
            patient = super().create(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(
                error, "error occurred while creating patient"
            )
            return handle_error_response(response, error)

        data = format_response_data(patient.data, 201, "patient created")

        cache.invalidate("patients")
        return Response(data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        try:
            patient = super().retrieve(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(patient.data, 200)

        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            patient = super().update(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(patient.data, 200)

        cache.invalidate("patients")
        return Response(data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.queryset
            patients = self.serializer_class(queryset, many=True)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(patients.data, 200)

        cache.set("patients", data)
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            patient = super().destroy(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(patient.data, 204)

        cache.invalidate("patients")
        return Response(data, status=status.HTTP_204_NO_CONTENT)
