from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.common import models as base_models
from apps.common.models import Currency, PriceType, RoleType
from apps.notifications.utils import fcm_notify_bulk

# Create your models here.


class Tag(base_models.BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Job(base_models.BaseModel):
    class LocationType(models.TextChoices):
        REMOTE = "remote", _("Remote")
        ONSITE = "on-site", _("On Site")
        HYBRID = "hybrid", _("Hybrid")

    class ApplicationType(models.TextChoices):
        INTERNAL = "internal", _("Internal")
        EXTERNAL = "external", _("External")

    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        INACTIVE = "inactive", _("Inactive")
        ASSIGNED = "assigned", _("Assigned")
        COMPLETED = "completed", _("Completed")

    class EscrowStatus(models.TextChoices):
        CREATED = "created", _("Created")
        REDEEMED = "redeemed", _("Redeemed")
        PENDING = "pending", _("Pending")

    company = models.ForeignKey(
        "companies.Company", on_delete=models.CASCADE, related_name="jobs"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    date = models.DateField(null=True)
    location = models.CharField(
        max_length=25, choices=LocationType.choices, default=LocationType.REMOTE
    )
    address = models.CharField(
        max_length=255,
        blank=True,
    )
    tags = models.ManyToManyField(Tag, blank=True)
    skills = models.ManyToManyField("users.Skill", blank=True)
    role_type = models.CharField(max_length=50, choices=RoleType.choices, blank=True)
    price_type = models.CharField(max_length=50, choices=PriceType.choices)
    price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    min_price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    max_price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
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
    escrow_status = models.CharField(
        max_length=25, choices=EscrowStatus.choices, default=EscrowStatus.PENDING
    )

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


class JobBookmark(base_models.BaseModel):
    freelancer = models.ForeignKey(
        "freelancers.Freelancer", on_delete=models.CASCADE, related_name="job_bookmarks"
    )
    job = models.ForeignKey("Job", on_delete=models.CASCADE, related_name="bookmarks")

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"Bookmarked {self.job.title}::{self.freelancer.user.username}"


class JobSubmission(base_models.BaseModel):
    application = models.ForeignKey(
        "Application", on_delete=models.CASCADE, related_name="submission"
    )
    freelancer = models.ForeignKey(
        "freelancers.Freelancer",
        on_delete=models.CASCADE,
        null=True,
        related_name="job_submissions",
    )
    link = models.CharField(max_length=500, blank=True)
    file = models.FileField(upload_to="job_submissions", null=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"Submission {self.application.job.title}::{self.application.freelancer.user.username}"


# SIGNALS
# ---------------------------------------------------
@receiver(models.signals.post_save, sender=Application)
def set_owner_role(sender, instance, created, **kwargs):
    from fcm_django.models import FCMDevice

    if created:
        freelancer = instance.freelancer
        job = instance.job
        company = job.company

        # send notification
        Q = models.Q
        devices = FCMDevice.objects.filter(
            Q(user__companies_managed__company=company) | Q(user__company=company)
        )
        title = "Job Application"
        body = f"{freelancer.fullname or 'User'} applied for the Job titled {job.title}"
        fcm_notify_bulk(title, body, devices=devices)
