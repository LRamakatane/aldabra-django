#!/usr/bin/env python3
"""login api view with knox"""
# REST FRAMEWORK
from rest_framework import permissions, generics, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from services.clients.oauthclient import get_employee
from services.exceptions import EmployeeNotFound

# KNOX
from knox.models import AuthToken

# serializers
from services.authservice.api.v1.serializers import UserSerializer, LoginUserSerializer

from services.exceptions import exception_handler
from services.exceptions import handle_error_response

import datetime

from django.conf import settings

import binascii
import os

from django.utils import timezone

from knox.settings import knox_settings
from rest_framework.views import APIView

from core.models import RefreshToken


def generate_60min_timestamp(min: int = 60):
    # Get the current time
    current_time = datetime.datetime.now()

    # Add 30 minutes to the current time
    time_in_minutes_from_now = current_time + datetime.timedelta(minutes=min)

    # Convert the result to a timestamp (Unix timestamp, which is the number of seconds since January 1, 1970)
    timestamp = int(time_in_minutes_from_now.timestamp())

    return timestamp


class LoginAPIView(generics.GenericAPIView):
    """
    logs a user in using a basic authentication method

    Args:
        email: user's email address
        password: user's password

    Returns: [user_object, auth_token]
    """

    authentication_classes = [BasicAuthentication]
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginUserSerializer

    def post(self, request, *args: tuple, **kwargs: dict) -> Response:
        """
        handles the post data sent to 'auth/api/v1/login'

        Args:
            request (object): clients request

        Returns:
            user: the user's object
            Token: user token
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data

        except Exception as error:
            response = exception_handler(
                exc=error, context="something went wrong while login you in"
            )
            return handle_error_response(response, error)

        try:
            request.user = user
            get_employee(request)
        except Exception as error:
            response = exception_handler(
                exc=error, context="something went wrong while login you in"
            )
            return handle_error_response(response, error)

        instance, auth_token = AuthToken.objects.create(user)
        refresh_token = self.create_refresh_token(instance)
        response = {
            "message": "Login Successful",
            "status_code": 200,
            "payload": {
                "user": UserSerializer(user).data,
                "token": auth_token,
                "refresh_token": refresh_token.refresh_token,
                "expire_at": generate_60min_timestamp(settings.TOKEN_EXPIRE_AT),
            },
        }

        return Response(response, status=status.HTTP_200_OK)

    def create_refresh_token(self, auth_token):
        # Generate a new refresh token
        refresh_token = binascii.hexlify(os.urandom(24)).decode()
        return RefreshToken.objects.create(
            auth_token=auth_token, refresh_token=refresh_token, user=auth_token.user
        )


class RefreshTokenView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Assuming the RefreshToken model has a `refresh_token` field
            refresh_token_instance = RefreshToken.objects.get(
                refresh_token=refresh_token
            )
            user = refresh_token_instance.user

            # Check if the token is expired
            if refresh_token_instance.is_expired:
                refresh_token_instance.delete()
                return Response(
                    {"error": "Refresh token has expired"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            instance, token = AuthToken.objects.create(user)

            # Optionally, create a new refresh token and delete the old one
            refresh_token_instance.delete()
            new_refresh_token = self.create_refresh_token(instance)

            return Response(
                {
                    "token": token,
                    "refresh_token": new_refresh_token.refresh_token,
                    "expire_at": generate_60min_timestamp(settings.TOKEN_EXPIRE_AT),
                }
            )

        except RefreshToken.DoesNotExist:
            return Response(
                {"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )

    def create_refresh_token(self, auth_token):
        # Generate a new refresh token
        refresh_token = binascii.hexlify(os.urandom(24)).decode()
        return RefreshToken.objects.create(
            auth_token=auth_token, refresh_token=refresh_token, user=auth_token.user
        )
