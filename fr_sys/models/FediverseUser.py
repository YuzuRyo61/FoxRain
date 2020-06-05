import uuid

from django.db import models
from django.core.validators import RegexValidator

from .FediverseServer import FediverseServer


class FediverseUser(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )
    id = models.URLField(
        unique=True
    )
    username = models.CharField(
        max_length=32,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_]+$"
            )
        ],
        editable=False
    )
    server = models.OneToOneField(
        FediverseServer,
        on_delete=models.CASCADE
    )
    display_name = models.CharField(
        max_length=255,
        blank=True
    )
    description = models.TextField(
        blank=True
    )
    is_bot = models.BooleanField(
        default=False
    )
    is_manualFollow = models.BooleanField(
        default=False
    )
    is_silence = models.BooleanField(
        default=False
    )
    is_suspend = models.BooleanField(
        default=False
    )
    inbox = models.URLField(
        unique=True
    )
    outbox = models.URLField(
        blank=True
    )
    featured = models.URLField(
        blank=True
    )
    followers = models.URLField(
        blank=True
    )
    following = models.URLField(
        blank=True
    )
    URL = models.URLField(
        blank=True
    )
    publicKey = models.TextField(
        editable=False,
        blank=True
    )
    KeyId = models.CharField(
        max_length=255,
        blank=True
    )
    registered = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"@{self.username}@{self.server}"
