from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common import models as base_models
from apps.common.models import HowYouFoundUs
from apps.users.models import phone_regex

User = get_user_model()


class Company(base_models.BaseModel):
    class CompanySize(models.TextChoices):
        SMALL = "small", _("Small")
        MEDIUM = "medium", _("Medium")
        BIG = "big", _("Big")

    class OrganizationType(models.TextChoices):
        PUBLIC_COMPANY = "public_company", _("Public Company")
        SELF_EMPLOYED = "self_employed", _("Self Employed")
        GOVERNMENT_AGENCY = "governmet_agency", _("Government Agency")
        NONPROFIT = "nonprofit", _("Non Profit")
        SOLE_PROPRIETORSHIP = "sole_proprietorship", _("Sole Proprietorship")
        PRIVATELY_HELD = "privately_held", _("Privately Help")
        PARTNERSHIP = "partnership", _("Partnership")

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    company_size = models.CharField(
        max_length=60, choices=CompanySize.choices, default=CompanySize.SMALL
    )
    organization_type = models.CharField(
        max_length=60,
        choices=OrganizationType.choices,
    )
    email = models.EmailField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=25, validators=[phone_regex], blank=True)
    website = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to="logos", blank=True, null=True)
    tagline = models.CharField(max_length=100, blank=True)
    how_you_found_us = models.CharField(
        max_length=100, choices=HowYouFoundUs.choices, default=HowYouFoundUs.OTHER
    )

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.name}"


class CompanyManager(base_models.BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies")
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="managers"
    )

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.user.username}::{self.company.name}"