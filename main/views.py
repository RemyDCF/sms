import hmac
import json
import os
import subprocess
from _sha1 import sha1

from django.conf import settings
from django.utils.encoding import force_bytes
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from ipaddress import ip_address, ip_network

import requests
from django.http import HttpResponseForbidden, HttpResponseServerError, HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "main.html")


@require_POST
@csrf_exempt
def deploy(request):
    # Verify if request came from GitHub.
    forwarded_for = u"{}".format(request.META.get("HTTP_X_FORWARDED_FOR"))
    client_ip_address = ip_address(forwarded_for)
    whitelist = requests.get("https://api.github.com/meta").json()["hooks"]

    for valid_ip in whitelist:
        if client_ip_address in ip_network(valid_ip):
            break
    else:
        return HttpResponseForbidden("Permission denied.")

    # Verify the request signature
    header_signature = request.META.get("HTTP_X_HUB_SIGNATURE")
    if header_signature is None:
        return HttpResponseForbidden("Permission denied.")

    sha_name, signature = header_signature.split("=")
    if sha_name != "sha1":
        return HttpResponseServerError("Operation not supported.", status=501)

    mac = hmac.new(
        force_bytes(settings.GITHUB_WEBHOOK_KEY),
        msg=force_bytes(request.body),
        digestmod=sha1,
    )
    if not hmac.compare_digest(force_bytes(mac.hexdigest()), force_bytes(signature)):
        return HttpResponseForbidden("Permission denied.")

    # If request reached this point we are in a good shape
    # Process the GitHub events
    event = request.META.get("HTTP_X_GITHUB_EVENT", "ping")

    if event == "ping":
        return HttpResponse("pong")
    elif event == "push":
        branch = json.loads(request.body)["ref"]
        if branch != "refs/heads/master":
            return HttpResponse("Wrong branch", status=418)
        subprocess.call(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "deploy.sh")
        )
        return HttpResponse("success")

    # In case we receive an event that's neither a ping or push
    return HttpResponse(status=204)
