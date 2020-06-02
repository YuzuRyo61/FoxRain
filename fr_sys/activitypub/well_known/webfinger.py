import re

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.http.response import (
    JsonResponse,
    HttpResponseNotFound
)


def webfinger(request):
    subject = request.GET.get('resource')
    if subject is None:
        return HttpResponseNotFound()

    subject_parse = re.search(r"^acct:(.+)@(.+)$", subject)
    if subject_parse is None:
        return HttpResponseNotFound()

    if settings.FR_ENDPOINT != subject_parse.group(2):
        return HttpResponseNotFound()

    userInfo = get_object_or_404(get_user_model(), username__iexact=subject_parse.group(1), is_active=True)

    return JsonResponse({
        "subject": f"acct:{userInfo.username}@{settings.FR_ENDPOINT}",
        "aliases": [
            f"https://{settings.FR_ENDPOINT}{reverse_lazy('AP:user', kwargs={'uuid': userInfo.uuid})}",
            # f"https://{settings.FR_ENDPOINT}"  # todo: specify user's endpoint
        ],
        "links": [
            {
                "rel": "self",
                "type": "application/activity+json",
                "href": f"https://{settings.FR_ENDPOINT}{reverse_lazy('AP:user', kwargs={'uuid': userInfo.uuid})}",
            },
            # {
            #     "rel": "http://webfinger.net/rel/profile-page",
            #     "type": "text/html",
            #     "href": f"https://{settings.FR_ENDPOINT}"  # todo: specify user's endpoint
            # },
            # {
            #     "rel": "http://ostatus.org/schema/1.0/subscribe",
            #     "template": f"https://{settings.FR_ENDPOINT}"  # todo: specify follow dialog endpoint
            # }
        ]
    })
