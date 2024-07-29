import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created_at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.pk)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.pk}>"

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save(update_fields=["is_active", "updated_at"] if self.pk else None)

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save(update_fields=["is_active", "updated_at"] if self.pk else None)


class PriceType(models.TextChoices):
    PER_PROJECT = "per_project", _("Per Project")
    PER_HOUR = "per_hour", _("Per Hour")
    PER_WEEK = "per_week", _("Per Week")
    PER_MONTH = "per_month", _("Per Month")


class HowYouFoundUs(models.TextChoices):
    FACEBOOK = "facebook", _("Facebook")
    TWITTER = "twitter", _("Twitter")
    INSTAGRAM = "instagram", _("Instagram")
    YOUTUBE = "youtube", _("Youtube")
    TECH_EVENT = "tech_event", _("Tech Event")
    AFRIBLOCK_MEMBER = "afriblock_member", _("AfriBlock Member")
    AFRIBLOCK_EMPLOYEE = "afriblock_employee", _("AfriBlock Employee")
    OTHER = "other", _("Other")


class Currency(models.TextChoices):
    USD = "USD", _("U.S Dollar")
    GHS = "GHS", _("Cedi")
    GBP = "GBP", _("British Pound")
    NGN = "NGN", _("Naira")
    KES = "KES", _("Kenyan shilling")
    ZAR = "ZAR", _("South African Rand")
    EUR = "EUR", _("Euro")
    CAD = "CAD", _("Canadian Dollar")
