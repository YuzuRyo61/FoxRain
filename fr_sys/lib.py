import base64
import hashlib
import logging
import requests
from urllib.parse import urlparse
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from json.decoder import JSONDecodeError
from requests_http_signature import HTTPSignatureHeaderAuth

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from FoxRain import __version__ as FR_VERSION

from fr_sys import models

logger = logging.getLogger("fr_sys.lib")


def generate_key():
    """
    Generate user key for local user signature
    (PrivateKey, PublicKey)
    :rtype: tuple
    """
    rsa = RSA.generate(4096, Random.new().read)
    return (rsa.exportKey().decode("utf-8"), rsa.publickey().exportKey().decode("utf-8"))


def sign_header(username):
    userInfo = get_user_model.objects.get(username__iexact=username)
    return HTTPSignatureHeaderAuth(
        algorithm="rsa-sha256",
        key=bytes(userInfo.privateKey, "UTF-8"),
        headers=["(request-target)", "host", "date"],
        key_id=f"https://{settings.FR_ENDPOINT}{reverse_lazy('AP:user', kwargs={'uuid': userInfo.uuid})}"
    )


def _signature_parse(signature):
    if signature is None:
        return None
    out = {}
    for data in signature.split(","):
        k, v = data.split("=", 1)
        out[k] = v[1 : len(v) - 1]  # noqa: E203
    return out


def _signature_body(signed_headers, method, path, headers, body_digest):
    out = []
    for signed_header in signed_headers.split(" "):
        if signed_header == "(request-target)":
            out.append("(request-target): " + method.lower() + " " + path)
        elif signed_header == "digest":
            out.append("digest: " + body_digest)
        else:
            out.append(signed_header + ": " + headers[signed_header])
    return "\n".join(out)


def _body_digest(body: str):
    bodyHash = hashlib.new("sha256")
    bodyHash.update(body)
    return "SHA-256=" + base64.b64encode(bodyHash.digest()).decode("utf-8")


def _signature_verify(signed_string, signature, publicKey):
    sign = PKCS1_v1_5.new(publicKey)
    digest = SHA256.new()
    digest.update(signed_string.encode("utf-8"))
    return sign.verify(digest, signature)


def verify_signature(request, targetUser, method="POST", path=None, signature=None, body=None):
    sign_parse = _signature_parse(signature)
    if sign_parse is None:
        logger.error("Signature parse failed")
        return False
    signed_string = _signature_body(
        sign_parse["headers"],
        method,
        path,
        request.headers,
        _body_digest(body)
    )

    if targetUser.KeyId != sign_parse["keyId"]:
        logger.error("Signature keyId does not match")
        return False

    return _signature_verify(signed_string, base64.b64decode(sign_parse["signature"]), targetUser.publicKey)


def addDefaultHeader(header={}, isGETMethod=False):
    header.update({
        "User-Agent": f"FoxRain/{str(FR_VERSION)}"
    })

    if isGETMethod:
        header.update({
            "Accept": "application/activity+json"
        })
    else:
        header.update({
            "Content-Type": "application/activity+json"
        })

    return header


def isAPContext(apbody: dict):
    if apbody.get("@context") is not None and type(apbody.get("@context")) == str:
        if apbody["@context"] != "https://www.w3.org/ns/activitystreams":
            return False
    elif apbody.get("@context") is not None and type(apbody.get("@context")) == list:
        if "https://www.w3.org/ns/activitystreams" not in apbody["@context"]:
            return False
    else:
        return False

    return True


def regFedUser(uri):
    try:
        requestRaw = requests.get(
            uri,
            headers=addDefaultHeader(isGETMethod=True)
        )
        requestRaw.raise_for_status()
        res = requestRaw.json()
        host = urlparse(uri).netloc
        if host == '':
            logger.error("unknown host")
            return None
        else:
            try:
                fediSrv = models.FediverseServer.objects.get(
                    address=host
                )
            except models.FediverseServer.DoesNotExist:
                fediSrv = models.FediverseServer(
                    address=host
                )

        if not isAPContext(res):
            logger.error("Response is not ActivityPub")
            return None

    except JSONDecodeError:
        logger.error("JSON parse error.")
        return None

    if res.get("publicKey") is not None:
        publicKey = res["publicKey"].get("publicKeyPem")
        keyId = res["publicKey"].get("id")
    else:
        logger.warn("The retrieved user does not have a signing key. Tampering may occur.")
        keyId = None
        publicKey = None

    if res.get("sharedInbox") is None:
        if res.get("endpoints") is not None and res["endpoints"].get("sharedInbox") is not None:
            sharedInbox = res["endpoints"].get("sharedInbox")
        else:
            sharedInbox = None
    else:
        sharedInbox = res["sharedInbox"]

    if sharedInbox is not None:
        fediSrv.sharedInbox = sharedInbox

    fediSrv.save()

    logger.info("New Fediverse user fetched.")
    return models.FediverseUser(
        id=res["id"],
        username=res["preferredUsername"],
        server=fediSrv,
        display_name=res.get("name"),
        description=res.get("summary"),
        is_bot=True if res["type"] == "Service" else False,
        is_manualFollow=res.get("manuallyApprovesFollowers", False),
        inbox=res["inbox"],
        outbox=res.get("outbox"),
        featured=res.get("featured"),
        followers=res.get("followers"),
        following=res.get("following"),
        URL=res.get("url"),
        publicKey=publicKey,
        KeyId=keyId
    )
