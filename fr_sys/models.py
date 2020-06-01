import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

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
        blank=True
    )
    description = models.TextField(
        blank=True
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
        editable=False
    )
    privateKey = models.TextField(
        editable=False
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


class FediverseServer(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )
    address = models.CharField(
        max_length=255,
        unique=True
    )
    is_block = models.BooleanField(
        default=False
    )
    is_deprecated = models.BooleanField(
        default=False
    )


class FediverseUser(models.Model):
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
    is_silence = models.BooleanField(
        default=False
    )
    is_suspend = models.BooleanField(
        default=False
    )
    publicKey = models.TextField(
        editable=False
    )
    registered = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )


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
        blank=True
    )
