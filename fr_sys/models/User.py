import uuid

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse_lazy

from fr_sys.lib import generate_key


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not username:
            raise ValueError("User must have an username")

        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        kp = generate_key()
        user.privateKey = kp[0]
        user.publicKey = kp[1]
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password
        )
        user.moderator = True
        user.administrator = True
        user.is_emailVerified = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )
    username = models.CharField(
        max_length=32,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_]+$"
            )
        ],
        unique=True,
        editable=False
    )
    email = models.EmailField(
        unique=True
    )
    display_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True
    )
    is_emailVerified = models.BooleanField(
        default=False
    )
    is_bot = models.BooleanField(
        default=False
    )
    is_silence = models.BooleanField(
        default=False
    )
    is_suspend = models.BooleanField(
        default=False
    )
    is_manualFollow = models.BooleanField(
        default=False
    )
    moderator = models.BooleanField(
        default=False
    )
    administrator = models.BooleanField(
        default=False
    )
    registered = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )
    publicKey = models.TextField(
        editable=False,
        unique=True
    )
    privateKey = models.TextField(
        editable=False,
        unique=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"@{self.username}"

    @property
    def is_staff(self):
        return self.moderator

    @property
    def is_superuser(self):
        return self.administrator

    @property
    def KeyId(self):
        return f"https://{settings.FR_ENDPOINT}{reverse_lazy('AP:user', kwargs={'uuid': self.uuid})}#main-key"
