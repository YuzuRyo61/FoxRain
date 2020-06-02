import json

from django.http.response import HttpResponse

from . import AP_HEADER


def ActivityPubResponse(request, bodyDict: dict):
    if bodyDict.get("@content") is None:
        bodyDict.update(AP_HEADER)

    content_type = "application/activity+json; charset=utf-8"
    if request.headers.get("accept", "").startswith("application/ld+json"):
        content_type = "application/ld+json; profile=\"https://www.w3.org/ns/activitystreams\"; charset=utf-8"

    return HttpResponse(
        json.dumps(
            bodyDict,
            ensure_ascii=False
        ),
        content_type=content_type,
        charset="utf-8"
    )
