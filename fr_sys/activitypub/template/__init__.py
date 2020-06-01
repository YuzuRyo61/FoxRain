from .request import isAPRequest
from .response import ActivityPubResponse

AP_HEADER = {
    "@content": [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/v1"
    ]
}


__all__ = [
    "ActivityPubResponse",
    "isAPRequest"
]
