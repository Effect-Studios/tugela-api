from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common import models as base_models
from apps.common.models import Currency, PriceType

# Create your models here.


class Tag(base_models.BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Job(base_models.BaseModel):
    class LocationType(models.TextChoices):
        REMOTE = "remote", _("Remote")
        ONSITE = "on-site", _("On Site")

    class ApplicationType(models.TextChoices):
        INTERNAL = "internal", _("Internal")
        EXTERNAL = "external", _("External")

    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        INACTIVE = "inactive", _("Inactive")
        ASSIGNED = "assigned", _("Assigned")
        COMPLETED = "completed", _("Completed")

    company = models.ForeignKey(
        "companies.Company", on_delete=models.CASCADE, related_name="jobs"
    )
    title = models.CharField(max_length=65)
    description = models.TextField(blank=True)
    date = models.DateField(null=True)
    location = models.CharField(
        max_length=25, choices=LocationType.choices, default=LocationType.REMOTE
    )
    address = models.CharField(
        max_length=255,
        blank=True,
    )
    tags = models.ManyToManyField(Tag, blank=True)
    skills = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    price_type = models.CharField(max_length=50, choices=PriceType.choices)
    price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    currency = models.CharField(
        max_length=20, choices=Currency.choices, default=Currency.XRP
    )
    status = models.CharField(
        max_length=25, choices=Status.choices, default=Status.ACTIVE
    )
    application_type = models.CharField(
        max_length=25, choices=ApplicationType.choices, default=ApplicationType.INTERNAL
    )
    external_apply_link = models.CharField(max_length=100, blank=True)
    escrow_sequence = models.CharField(max_length=255, blank=True)
    escrow_condition = models.CharField(max_length=255, blank=True)
    escrow_fulfillment = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.title}::{self.company.name}"


class Application(base_models.BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        ACCEPTED = "accepted", _("Accepted")
        REJECTED = "rejected", _("Rejected")

    freelancer = models.ForeignKey(
        "freelancers.Freelancer", on_delete=models.CASCADE, related_name="applications"
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applicants")
    status = models.CharField(
        max_length=25, choices=Status.choices, default=Status.PENDING
    )

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.job.title}::{self.freelancer.user.username}"
