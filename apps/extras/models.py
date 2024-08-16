from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.common import models as base_models


# Validator function to check if string is interger
def validate_integer(value):
    if not value.isdigit():
        raise ValidationError({"detail": _("Not a valid integer")})


class Currency(base_models.BaseModel):
    class Type(models.TextChoices):
        FIAT = "fiat", _("Fiat")
        CRYPTO = "crypto", _("Crypto")

    code = models.CharField(max_length=3, unique=True)
    factor = models.CharField(max_length=64, validators=[validate_integer])
    name = models.CharField(max_length=64)
    precision = models.PositiveSmallIntegerField(default=0)
    symbol = models.CharField(max_length=2, null=True, blank=True)
    _type = models.CharField(max_length=10, choices=Type.choices, default=Type.FIAT)

    def __str__(self):
        return f"{self.name}::{self.code}"


class Country(base_models.BaseModel):
    code = models.CharField(max_length=10)
    iso = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}::{self.code}"
