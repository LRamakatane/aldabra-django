# /usr/bin/env python3
"""oauthclient
inherits from APIClient, used for connecting to Ouath
protected resources.
"""
from .oauthclient import OAuthClient


class ZohoMailClient(OAuthClient):
    """oauth client

    Usage
    -----
    - inilize client, this attemps to get an access token;
        system = System.objects.all()[0]
        new_client = ZohoMailClient(system=system, grant_type='client_credentials')

    - if successful, the client should have an access token, then make a request
        req = new_client.make_request(method='get', resource_path='/orders/')

    - if access token expires, use refresh token to get a new one
        new_client.get_access_token(system=system, grant_type='refresh_token')

    - if you want to use a different system, you can change it
        new_client.system = new_system

    - if you want to use a different access token, you can change it
        new_client.access_token = new_access_token

    - if you want to use a different refresh token, you can change it
        new_client.refresh_token = new_refresh_token


    Initialization
    --------------
    system: core.models.System
        system object that holds all the system information
    grant_type: str
        grant type to use, default is 'client_credentials'
    scope: str
        scope to use, default is ''


    Superclass
    ----------
    services.clients.OAuthClient

    """

    def __init__(
        self,
        system: object,
        grant_type="refresh_token",
        scope="ZohoMail.messages.CREATE",
    ) -> None:
        super().__init__(system, grant_type=grant_type, scope=scope)
        self.refresh_token = self.system["refresh_token"]

    def send_mail(
        self,
        from_address: str,
        to: str,
        subject: str,
        content: str,
        accountId,
        cc="",
        bcc="",
        ask_receipt="yes",
        method="post",
        resource_path="/",
        headers=None,
    ):
        h = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}
        if headers:
            h = h.update(headers)
        else:
            headers = h

        data = {
            "fromAddress": from_address,
            "toAddress": to,
            "ccAddress": cc,
            "bccAddress": bcc,
            "subject": subject,
            "content": content,
            "askReceipt": ask_receipt,
        }
        self.base_url = f"https://mail.zoho.com/api/accounts/{accountId}"
        super().request(
            method=method, resource_path=resource_path, data=data, headers=h
        )
