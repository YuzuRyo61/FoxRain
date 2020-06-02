import requests
from Crypto.PublicKey import RSA
from Crypto import Random
from requests_http_signature import HTTPSignatureHeaderAuth

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from FoxRain import __version__ as FR_VERSION


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


def __signature_resolver(key_id, algorithm):
    print(key_id)
    print(algorithm)


def verify_signature(request):
    session = requests.Session()
    session.headers["Authorization"] = "Signature " + request.headers["Signature"]
    HTTPSignatureHeaderAuth.verify(session, __signature_resolver)


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
