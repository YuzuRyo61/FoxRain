from django.conf import settings
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseGone
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from .template import AP_HEADER, ActivityPubResponse, isAPRequest


def User(request, uuid):
    userInfo = get_object_or_404(get_user_model(), uuid=uuid)

    if not userInfo.is_active:
        return HttpResponseGone()

    if not isAPRequest(request):
        return redirect(f"/@{userInfo.username}")  # to-do: redirect to web profile page

    return ActivityPubResponse(request, {
        **AP_HEADER,
        "type": "Service" if userInfo.is_bot else "Person",
        "id": f"https://{settings.FR_ENDPOINT}{reverse_lazy('AP:user', kwargs={'uuid': userInfo.uuid})}",
        "inbox": f"https://{settings.FR_ENDPOINT}{reverse_lazy('AP:inbox', kwargs={'uuid': userInfo.uuid})}",
        # "outbox": f"https://{settings.FR_ENDPOINT}{reverse_lazy('AP:outbox', kwargs={'uuid': userInfo.uuid})}",
        # "followers": f"https://{settings.FR_ENDPOINT}{reverse_lazy('AP:followers', kwargs={'uuid': userInfo.uuid})}",
        # "following": f"https://{settings.FR_ENDPOINT}{reverse_lazy('AP:following', kwargs={'uuid': userInfo.uuid})}",
        # "featured": f"https://{settings.FR_ENDPOINT}{reverse_lazy('AP:featured', kwargs={'uuid': userInfo.uuid})}",
        # "sharedInbox": f"https://{settings.FR_ENDPOINT}{reverse_lazy('AP:inbox_share', kwargs={'uuid': userInfo.uuid})}",
        # "endpoints": {
        # "sharedInbox": f"https://{settings.FR_ENDPOINT}{reverse_lazy('AP:inbox_share', kwargs={'uuid': userInfo.uuid})}"
        # }
        "url": f"https://{settings.FR_ENDPOINT}/@{userInfo.username}",  # to-do: public page
        "preferredUsername": userInfo.username,
        "name": None if userInfo.display_name == "" else userInfo.display_name,
        "summary": None if userInfo.description == "" else userInfo.description,
        "manuallyApprovesFollowers": userInfo.is_manualFollow,
        "publicKey": {
            "id": f"https://{settings.FR_ENDPOINT}{reverse_lazy('AP:user', kwargs={'uuid': userInfo.uuid})}#main-key",
            "type": "Key",
            "owner": f"https://{settings.FR_ENDPOINT}{reverse_lazy('AP:user', kwargs={'uuid': userInfo.uuid})}",
            "publicKeyPem": userInfo.publicKey
        }
    })
