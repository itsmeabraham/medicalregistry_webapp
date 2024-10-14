from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.exports.models import ExportableModel
from base.models import TimeStampedModel, UUIDModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, UUIDModel, TimeStampedModel):
    """
    User Model
    """

    email = models.EmailField(max_length=255, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class UserExport(ExportableModel):
    """
    Model for User Exports
    """

    from .resources import UserResource

    EXPORT_RESOURCE = UserResource
    FILTER_FIELDS_MAP = {"created_at__date__gte": "start_date", "created_at__date__lte": "end_date"}

    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    class Meta:
        ordering = ["created_at"]
