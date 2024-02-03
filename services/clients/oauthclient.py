# /usr/bin/env python3
"""oauthclient
inherits from APIClient, used for connecting to Ouath
protected resources.
"""
from .apiclient import APIClient
from services.utils.cache import Cache
from typing import Any
from services.exceptions import EmployeeNotFound

from config.settings import getvar

cache = Cache(timeout=3600)


class OAuthClient(APIClient):
    __access_token: str = ""
    __refresh_token: str = ""
    __system: Any

    def __init__(self, system: Any, grant_type="client_credentials", scope="") -> None:
        self.__system = system
        super().__init__(self.__system["url_endpoint"], "oauth")
        self.access_token = cache.get(f"access_token_{system['sid']}")
        self.refresh_token = cache.get(f"refresh_token_{system['sid']}")

        if self.access_token is None:
            print("trying to get token")
            self.get_access_token(
                system=self.__system, grant_type=grant_type, scope=scope
            )
            self.refresh_token = self.json.get("refresh_token", None)
            self.access_token = self.json.get("access_token", None)
            cache.set(f"access_token_{system['sid']}", self.access_token)
            cache.set(f"refresh_token_{system['sid']}", self.refresh_token)

    def refresh_token_grant_request(
        self,
        refresh_token,
        client_id,
        client_secret,
        redirect_uri,
        scope,
        send_data_as_params=True,
    ):
        d = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "scope": scope,
        }
        if send_data_as_params:
            request_params = f"?grant_type={d['grant_type']}&refresh_token={d['refresh_token']}&client_id={d['client_id']}&client_secret={d['client_secret']}&redirect_uri={d['redirect_uri']}&scope={d['scope']}"
            self.request(
                method="post",
                resource_path=self.system["refresh_endpoint"] + request_params,
            )
        else:
            self.request(
                method="post", resource_path=self.system["refresh_endpoint"], data=d
            )

    def client_credentials_grant_request(
        self,
        client_id,
        client_secret,
        redirect_uri,
        send_data_as_params=False,
        scope=None,
    ):
        d = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        }
        self.request(method="post", resource_path=self.system["token_endpoint"], data=d)

    def password_grant_request(
        self, client_id, client_secret, username, password, redirect_uri, scope=None
    ):
        d = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        }
        self.request(method="post", resource_path=self.system["token_endpoint"], data=d)

    def get_access_token(self, system: Any, grant_type: str, scope=""):
        """tries to fetch access token from endpoint"""
        if grant_type == "client_credentials":
            print("client_credentials")
            self.client_credentials_grant_request(
                system["system_client_id"],
                system["system_client_secret"],
                system["redirect_uri"],
            )

        elif grant_type == "password":
            self.password_grant_request(
                system["system_client_id"],
                system["system_client_secret"],
                system["admin_username"],
                system["admin_password"],
                system["redirect_uri"],
            )

        elif grant_type == "refresh_token":
            self.refresh_token_grant_request(
                refresh_token=system["refresh_token"],
                client_id=system["system_client_id"],
                client_secret=system["system_client_secret"],
                redirect_uri=system["redirect_uri"],
                scope=scope,
            )

    def make_request(self, method="get", resource_path="/", data=None, headers=None):
        h = {
            "content_type": "application/json",
            "authorization": f"Bearer {self.access_token}",
        }
        self.request(method=method, resource_path=resource_path, data=data, headers=h)

    @property
    def access_token(self):
        return self.__access_token

    @access_token.setter
    def access_token(self, new_access_token):
        self.__access_token = new_access_token

    @property
    def refresh_token(self):
        return self.__refresh_token

    @refresh_token.setter
    def refresh_token(self, new_refresh_token):
        self.__refresh_token = new_refresh_token

    @property
    def system(self):
        return self.__system

    @system.setter
    def system(self, new_system):
        self.__system = new_system


def get_app() -> dict:
    app = {
        "sid": getvar("sid"),
        "url_endpoint": getvar("url_endpoint"),
        "system_client_id": getvar("system_client_id"),
        "system_client_secret": getvar("system_client_secret"),
        "token_endpoint": getvar("token_endpoint"),
        "redirect_uri": getvar("redirect_uri"),
    }
    return app


def get_employee(request):
    """Use this to get the data of the employee from the IAM service"""

    response = cache.get(f"iam_user_{request.user.id}")

    print(response, "Response 30")

    try:
        if response is None:
            system = get_app()

            client = OAuthClient(system=system, grant_type="client_credentials")

            client.make_request(
                method="get",
                resource_path=f"/iam/accounts/{request.user.id}/account_info/",
            )
            if client.status_code == 200:
                response = client.json.get("payload")
                print("successfully fetched account info")

            else:
                print(
                    f"failed to fetch account info {str(request.user.id)[:8]}-****-****-****-************, operation aborted"
                )
                raise EmployeeNotFound(
                    f"Access Denied: failed to fetch account info {str(request.user.id)[:8]}-****-****-****-************, not an employee, operation aborted"
                )

            cache.set(f"iam_user_{request.user.id}", response)

        request.iam_user = response  # Set the data to a variable in the request object called request.iam_user
    except Exception as e:
        raise e
