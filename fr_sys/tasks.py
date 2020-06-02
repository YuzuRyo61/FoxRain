from __future__ import absolute_import, unicode_literals
from pprint import pformat
import logging

from celery import shared_task
import requests

from fr_sys.lib import sign_header, addDefaultHeader, verify_signature

logger = logging.getLogger("fr_sys.tasks")


@shared_task(default_retry_delays=180)
def sendAPData(targetUrl: str, fromUser: str, body: dict):
    logger.info(f"Sending ActivityPub data: {targetUrl}")
    logger.debug("Data: ")
    logger.debug(pformat(targetUrl))
    try:
        res = requests.post(
            targetUrl,
            json=body,
            auth=sign_header(fromUser),
            headers=addDefaultHeader()
        )
        res.raise_for_status()
    except Exception as e:
        logging.error("Error response returned.")
        raise sendAPData.retry() from e
    else:
        return res.status_code


@shared_task()
def processInbox(request, body, targetUser=None):
    verify_signature(request)
    return
