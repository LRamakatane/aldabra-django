"""handles responses v1
"""
from rest_framework.response import Response
from rest_framework import status
from services.exceptions.errors import *
import traceback
from services.utils.systems import get_app
from services.clients.zohomail import ZohoMailClient
from config.settings import getvar


def handle_error_response(response, error, exception=True) -> Response:
    summary = traceback.StackSummary.extract(traceback.walk_stack(None))

    print(response)

    if response is not None and isinstance(response.data, dict):
        response.data["status_code"] = response.status_code
        response.data["error"] = str(error)

    elif response is not None and isinstance(response.data, list):
        response.data = {
            "status_code": response.status_code,
            "error": response.data,
            "detail": str(error),
        }

    else:
        # ------- send invoice to customer mail ----------------
        response = Response(
            {
                "status_code": 503,
                "message": "Service is down or unavailable",
                "error": str(error),
                "traceback": "".join(summary.format()),
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
            exception=exception,
        )

        # ----- try send a mail to dev ----
        try:
            environment = getvar("ENV")
            if environment in ("dev", "local"):
                panic = ", so there's no cause for panic, this is probably a test"
            else:
                panic = ". Panic! Panic! Panic! Panic!"

            # -- get system, initialize mail client
            # and get account id --
            system = get_app("zoho_client")
            mail = ZohoMailClient(system=system)
            account_id = system.get("config").get("accountId")

            # -- build content,
            # and send email to email list --
            content = f"""
<head>
<style>
code {{
  font-family: Consolas,"courier new";
  color: crimson;
  background-color: #f1f1f1;
  padding: 2px;
  font-size: 105%;
}}
</style>
</head>
<p>Hi Devs,</p>

<p>I caught some unhandled errors/exceptions in the booking system. I threw some 5xx Service Unavailable for the meantime, so you should check that out.</p>
<p>The exception occurred in the {environment} environment{panic}.</p>

<p>Error detail: <code>{str(error)}</code></p>
<p>Traceback:
<pre>
  <code>
  {''.join(summary.format())}
  </code>
</pre>
</p>
"""
            addresses = [
                "ahmid.balogun@shipa.ng",
                "hadiza.mamudu@shipa.ng",
                "david.christopher@shipa.ng",
                "desmond.nnebue@shipa.ng",
            ]
            cc = ", ".join(addresses[1:])

            if environment in ["beta", "prod", "production"]:
                mail.send_mail(
                    from_address="techteam@aajexpress.org",
                    to=addresses[0],
                    cc=cc,
                    subject="server errors in booking system",
                    content=content,
                    accountId=account_id,
                    method="post",
                    resource_path="/messages",
                )

                # -- check for email status --
                if mail.status_code not in ("404", "400", "500"):
                    print("error email was sent successfully!")

        except Exception as error:
            print(error)

    return response
