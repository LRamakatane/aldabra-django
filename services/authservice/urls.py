#!/usr/bin/env python3
"""auth service url mapping"""
from django.urls import path

# rest framework default api router
from rest_framework.routers import DefaultRouter

# views and viewsets
from services.authservice.api.v1.endpoints import (
    UserViewset,
    LoginAPIView,
    RefreshTokenView
)

# knox views
from knox import views as knox_views

app_name = 'auth_service_v1'

router = DefaultRouter()
router.register('users', UserViewset, basename='users')

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh_token'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]
urlpatterns += router.urls
