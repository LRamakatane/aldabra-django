from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions, authentication  # new

from drf_yasg.views import get_schema_view  # new
from drf_yasg import openapi

import oauth2_provider.views as oauth2_views
from config.backends import TokenAPI
import debug_toolbar

schema_view = get_schema_view(
    openapi.Info(
        title="Aldabra AI",
        default_version="v1",
        description="Aldabra AI",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(authentication.BasicAuthentication,),
)


v1 = [
    path('auth/', include('services.authservice.urls', 'auth_service_v1'))
]

# oauth url mapping
# OAuth2 provider endpoints
oauth2_endpoint_views = [
    path("authorize/", oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path("token/", TokenAPI.as_view(), name="token"),
    path("revoke-token/", oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        path("applications/", oauth2_views.ApplicationList.as_view(), name="list"),
        path(
            "applications/register/",
            oauth2_views.ApplicationRegistration.as_view(),
            name="register",
        ),
        path(
            "applications/<pk>/",
            oauth2_views.ApplicationDetail.as_view(),
            name="detail",
        ),
        path(
            "applications/<pk>/delete/",
            oauth2_views.ApplicationDelete.as_view(),
            name="delete",
        ),
        path(
            "applications/<pk>/update/",
            oauth2_views.ApplicationUpdate.as_view(),
            name="update",
        ),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        path(
            "authorized-tokens/",
            oauth2_views.AuthorizedTokensListView.as_view(),
            name="authorized-token-list",
        ),
        path(
            "authorized-tokens/<pk>/delete/",
            oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete",
        ),
    ]


urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/v1/", include(v1), name="v1"),
    path(
        "api/v1/o/",
        include(
            (oauth2_endpoint_views, "oauth2_provider"), namespace="oauth2_provider"
        ),
    ),
]


debug_toolbar_urls = debug_toolbar.urls

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar_urls)),
        path("admin/", admin.site.urls),
    ]
