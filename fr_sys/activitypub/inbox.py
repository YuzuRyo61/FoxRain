import logging
import json
from pprint import pformat

from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from fr_sys.lib import verify_signature
# from fr_sys.tasks import processInbox
from fr_sys.activitypub.template.request import isAPRequestContent
from fr_sys.models import FediverseUser
from fr_sys.lib import isAPContext, regFedUser

logger = logging.getLogger("fr_sys.activitypub.inbox")


@csrf_exempt
def Inbox(request, uuid=None):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST")

    if not isAPRequestContent(request):
        return HttpResponseBadRequest()

    try:
        apbody = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        logger.error("JSON decode error")
        return HttpResponseBadRequest()

    if not isAPContext(apbody):
        logger.error("This is not ActivityPub body")
        return HttpResponseBadRequest()

    logger.debug("Recieved Activity: ")
    logger.debug(pformat(apbody))

    try:
        fromUsr = FediverseUser.objects.get(id=apbody["actor"])
        logger.debug("This user is known")
    except FediverseUser.DoesNotExist:
        logger.debug("This user doesn't known, creating.")
        fromUsr = regFedUser(apbody["actor"])
        if fromUsr is None:
            return HttpResponseBadRequest()
        else:
            fromUsr.save()

    if not verify_signature(request.method, request.path, request.headers, request.body):
        logger.error("Signature verification failed.")
        return HttpResponseBadRequest()

    return HttpResponse(status=202)
