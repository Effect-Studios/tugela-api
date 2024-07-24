from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.common import models as base_models

phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
    "allowed.",
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with given email and password
        """
        if not email:
            raise ValueError(_("The email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(PermissionsMixin, base_models.BaseModel, AbstractBaseUser):
    """Default user for api_project."""

    class Roles(models.TextChoices):
        MANAGER = "manager", _("Manager")
        ADMIN = "admin", _("Admin")
        USER = "user", _("User")

    class AccountType(models.TextChoices):
        COMPANY = "company", _("Company")
        FREELANCER = "freelancer", _("Freelancer")
        ADMIN = "admin", _("Admin")

    email = models.EmailField(unique=True, max_length=255, blank=False, null=False)
    #: First and last name do not cover name patterns around the globe
    username = models.CharField(_("Username"), blank=True, max_length=255)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into the admin site"),
    )
    role = models.CharField(max_length=25, choices=Roles.choices, default=Roles.USER)
    account_type = models.CharField(
        max_length=25, choices=AccountType.choices, null=True
    )
    deleted = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        ordering = ("created_at",)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.email

    def __str__(self) -> str:
        return self.get_full_name() or self.email


class Address(base_models.BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address_name = models.CharField(max_length=50)
    street_name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True)
    town = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    lat = models.DecimalField(max_digits=11, decimal_places=8, default=0)
    lon = models.DecimalField(max_digits=11, decimal_places=8, default=0)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.user.username}::{self.address_name}"


class Profile(base_models.BaseModel):
    class Gender(models.TextChoices):
        MALE = "m", "Male"
        FEMALE = "f", "Female"
        OTHER = "o", "Other"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255, blank=True)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, blank=True, null=True
    )
    gender = models.CharField(max_length=2, choices=Gender.choices)
    dob = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=25, validators=[phone_regex], blank=True)
    profile_image = models.ImageField(upload_to="profile", blank=True, null=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.user.username}'s profile"


# SIGNALS
# ---------------------------------------------------
@receiver(models.signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
