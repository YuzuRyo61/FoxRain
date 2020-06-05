import uuid

from django.db import models

from .FediverseServer import FediverseServer


class Emoji(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )
    name = models.CharField(
        max_length=255
    )
    remote = models.ForeignKey(
        FediverseServer,
        on_delete=models.CASCADE,
        blank=True,
        related_name="emojis"
    )
