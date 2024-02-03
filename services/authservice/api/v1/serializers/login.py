#!/usr/bin/env python3
"""login serializer"""
from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginUserSerializer(serializers.Serializer):
    """User login serializer"""
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, credentials: dict):
        """
        validates login data

        Args:
            credentials [dict]: user loging credentials

        Returns:
            user [dic]: user sirialized data
        """
        user = authenticate(**credentials)
        if user:
            # check if user is active
            # if user.is_active:
            return user
            # return {'warnings': 'inactive user', 'user': user}
        raise serializers.ValidationError('Invalid Credentials or User is inactive')
