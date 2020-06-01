from Crypto.PublicKey import RSA
from Crypto import Random

# from requests_http_signature import HTTPSignatureHeaderAuth


def generate_key():
    """
    Generate user key for local user signature
    (PrivateKey, PublicKey)
    :rtype: tuple
    """
    rsa = RSA.generate(4096, Random.new().read)
    return (rsa.exportKey().decode("utf-8"), rsa.publickey().exportKey().decode("utf-8"))
