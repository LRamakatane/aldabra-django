from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from core.models import Hospital

from services.hospitals.api.v1.serializers import HospitalSerializer

from services.utils import Cache, format_response_data
from services.exceptions import exception_handler, handle_error_response

cache = Cache()


class HospitalAPIView(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HospitalSerializer

    def create(self, request, *args, **kwargs):
        try:
            hospital = super().create(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(error, "error occurred while creating hospital")
            return handle_error_response(response, error)

        data = format_response_data(hospital.data, 201, "hospital created")

        cache.invalidate("hospitals")
        return Response(data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        try:
            hospital = super().retrieve(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(hospital.data, 200)

        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            hospital = super().update(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(hospital.data, 200)

        cache.invalidate("hospitals")
        return Response(data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.queryset.latest('-created_at')
            hospitals = self.serializer_class(queryset, many=True)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(hospitals.data, 200)

        cache.set("hospitals", data)
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            hospital = super().destroy(request, *args, **kwargs)
        except Exception as error:
            response = exception_handler(error, "error occurred")
            return handle_error_response(response, error)

        data = format_response_data(hospital.data, 204)

        cache.invalidate("hospitals")
        return Response(data, status=status.HTTP_204_NO_CONTENT)
