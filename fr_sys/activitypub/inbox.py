import logging
import json
from pprint import pformat

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from fr_sys.tasks import processInbox
from fr_sys.activitypub.template.request import isAPRequestContent

logger = logging.getLogger("fr_sys.activitypub.inbox")


@csrf_exempt
def Inbox(request, uuid=None):
    if not isAPRequestContent(request):
        return HttpResponseBadRequest()

    try:
        apbody = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        logger.error("JSON decode error")
        return HttpResponseBadRequest()

    logger.debug("Recieved Activity: ")
    logger.debug(pformat(apbody))

    processInbox.delay(request, apbody)
    return HttpResponse(status=202)
