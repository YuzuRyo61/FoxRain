AP_HEADER = {
    "@content": [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/v1"
    ]
}

from .request import isAPRequest  # noqa: E402
from .response import ActivityPubResponse  # noqa: E402

__all__ = [
    "ActivityPubResponse",
    "isAPRequest",
    "AP_HEADER"
]
