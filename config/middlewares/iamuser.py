#!/usr/bin/env python3


from services.clients.oauthclient import OAuthClient
from config.settings import getvar


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


class IAMUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        system = get_app()

        client = OAuthClient(system=system, grant_type="client_credentials")
        try:
            client.make_request(
                method="get",
                resource_path=f"/iam/accounts/{request.user.id}/account_info/",
            )
            if client.status_code == 200:
                response = client.json
                print("successfully fetched account info")
                request.iam_user = response  # Set the data to a variable in the request object called request.iam_user
                print(request.iam_user)
            else:
                print(
                    f"failed to fetch account info {request.user.id}, operation aborted"
                )
                raise Exception(
                    f"failed to fetch account info {request.user.id}, operation aborted"
                )
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
