from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.models import Application
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from oauth2_provider.views.base import TokenView


class OAuth2ClientCredentialAuthentication(OAuth2Authentication):
    """
    OAuth2Authentication doesn't allows credentials to belong to an application (client).
    This override authenticates server-to-server requests, using client_credential authentication.
    """

    def authenticate(self, request):
        authentication = super().authenticate(request)

        if authentication is not None:
            user, access_token = authentication
            if self._grant_type_is_client_credentials(access_token):
                authentication = access_token.application.user, access_token

        return authentication

    def _grant_type_is_client_credentials(self, access_token):
        return (
            access_token.application.authorization_grant_type
            == Application.GRANT_CLIENT_CREDENTIALS
        )


class TokenAPI(TokenView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 400:
            return JsonResponse({"detail": _("Invalid credentials given.")}, status=400)
        return response
