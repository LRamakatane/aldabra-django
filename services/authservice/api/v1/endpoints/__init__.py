#!/usr/bin/env python3
"""auth service v1 endpoints initialization"""
from services.authservice.api.v1.endpoints.users import UserViewset, UserRegistrationAPIView
from services.authservice.api.v1.endpoints.login import LoginAPIView, RefreshTokenView
from services.authservice.api.v1.endpoints.token import TokenAPI