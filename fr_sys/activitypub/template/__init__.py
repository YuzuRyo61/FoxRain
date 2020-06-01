AP_HEADER = {
    "@content": [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/v1"
    ]
}

from .response import ActivityPubResponse
from .request import isAPRequest

__all__ = [
    "ActivityPubResponse",
    "isAPRequest"
]
