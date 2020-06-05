import uuid

from django.db import models


class FediverseServer(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )
    address = models.CharField(
        max_length=255,
        unique=True
    )
    sharedInbox = models.URLField(
        blank=True,
        null=True
    )
    is_block = models.BooleanField(
        default=False
    )
    is_deprecated = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.address
