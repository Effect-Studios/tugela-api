from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.common import models as base_models
from apps.common.models import Currency, HowYouFoundUs

# Create your models here.
User = get_user_model()


class Freelancer(base_models.BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    how_you_found_us = models.CharField(
        max_length=100, choices=HowYouFoundUs.choices, default=HowYouFoundUs.OTHER
    )

    def __str__(self):
        return self.user.username


class WorkExperience(base_models.BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(
        "Freelancer", on_delete=models.CASCADE, related_name="work_experiences"
    )
    job_title = models.CharField(max_length=50)
    job_description = models.TextField(blank=True)
    company_name = models.CharField(max_length=50)
    currently_working_here = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.user.username}::{self.job_title}"


class PortfolioItem(base_models.BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(
        "Freelancer", on_delete=models.CASCADE, related_name="portfolio_item"
    )
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    category = models.ForeignKey("users.Category", on_delete=models.SET_NULL, null=True)
    skills = models.ManyToManyField("users.Skill")
    project_url = models.CharField(max_length=100, blank=True)
    video_url = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    portfolio_file = models.FileField(upload_to="portfolio", blank=True, null=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.freelancer.user.username}::{self.title}"


class Service(base_models.BaseModel):
    class PriceType(models.TextChoices):
        PER_PROJECT = "per_project", _("Per Project")
        PER_HOUR = "per_hour", _("Per Hour")
        PER_WEEK = "per_week", _("Per Week")
        PER_MONTH = "per_month", _("Per Month")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(
        "Freelancer", on_delete=models.CASCADE, related_name="services"
    )
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    category = models.ForeignKey("users.Category", on_delete=models.SET_NULL, null=True)
    skills = models.ManyToManyField("users.Skill")
    delivery_time = models.CharField(
        max_length=50, blank=True, help_text=_("E.g 3 days")
    )
    price_type = models.CharField(max_length=50, choices=PriceType.choices)
    starting_price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    currency = models.CharField(
        max_length=20, choices=Currency.choices, default=Currency.USD
    )
    service_image = models.ImageField(upload_to="services", blank=True, null=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.freelancer.user.username}::{self.title}"


# SIGNALS
# ---------------------------------------------------
@receiver(models.signals.post_save, sender=Freelancer)
def update_account_type(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.account_type = user.AccountType.FREELANCER
        user.save(update_fields=["account_type", "updated_at"])