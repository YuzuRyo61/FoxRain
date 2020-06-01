import json

from django.http.response import HttpResponse

from . import AP_HEADER


def ActivityPubResponse(bodyDict: dict):
    if bodyDict.get("@content") is None:
        bodyDict.update(AP_HEADER)

    return HttpResponse(
        json.dumps(
            bodyDict,
            ensure_ascii=False
        ),
        content_type="application/activity+json; charset=utf-8",
        charset="utf-8"
    )
