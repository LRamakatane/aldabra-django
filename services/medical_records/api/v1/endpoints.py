from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from core.models import MedicalRecord

from services.medical_records.api.v1.serializers import MedicalRecordSerializer

from services.utils import Cache, format_response_data
from services.exceptions import exception_handler, handle_error_response

cache = Cache()


class MedicalRecordAPIView(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MedicalRecordSerializer

    def create(self, request, *args, **kwargs):
        try:
            medical_record = super().create(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(
                error, "error occurred while creating medical_record"
            )
            return handle_error_response(response, error)

        data = format_response_data(medical_record.data, 201, "medical_record created")

        cache.invalidate("medical_records")
        return Response(data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        try:
            medical_record = super().retrieve(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(medical_record.data, 200)

        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            medical_record = super().update(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(medical_record.data, 200)

        cache.invalidate("medical_records")
        return Response(data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.queryset.latest("-created_at")
            medical_records = self.serializer_class(queryset, many=True)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(medical_records.data, 200)

        cache.set("medical_records", data)
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            medical_record = super().destroy(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(medical_record.data, 204)

        cache.invalidate("medical_records")
        return Response(data, status=status.HTTP_204_NO_CONTENT)
