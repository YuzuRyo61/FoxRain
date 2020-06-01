"""
 for ActivityPub router
"""

from django.urls import path

from .user import User
from .inbox import Inbox
from .outbox import Outbox
from .following import Following
from .followers import Followers
from .featured import Featured

app_name = "AP"

urlpatterns = [
    path("user/<uuid:uuid>", User, name="user"),
    path("user/<uuid:uuid>/inbox", Inbox, name="inbox"),
    path("user/<uuid:uuid>/outbox", Inbox, name="outbox"),
    path("user/<uuid:uuid>/following", Following, name="following"),
    path("user/<uuid:uuid>/followers", Followers, name="followers"),
    path("user/<uuid:uuid>/featured", Featured, name="featured"),
]
