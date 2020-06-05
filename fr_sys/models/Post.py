import uuid

from django.db import models

from django_currentuser.db.models import CurrentUserField

# from .Emoji import Emoji  # TBC
from .FediverseUser import FediverseUser


class Post(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )
    body = models.TextField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    post_by = CurrentUserField(
        related_name="post",
        blank=True
    )
    post_by_fed = models.ForeignKey(
        FediverseUser,
        on_delete=models.CASCADE,
        related_name="post"
    )
