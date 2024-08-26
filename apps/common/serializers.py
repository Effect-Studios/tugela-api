from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.companies.models import Company, CompanyIndustry, CompanyManager, CompanyValue
from apps.freelancers.models import Freelancer

User = get_user_model()


class UserBaseSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name"]

    def get_first_name(self, obj):
        return obj.profile.first_name

    def get_last_name(self, obj):
        return obj.profile.last_name


class FreelancerBaseSerializer(serializers.ModelSerializer):
    user = UserBaseSerializer()
    total_applications = serializers.SerializerMethodField()
    accepted_applications = serializers.SerializerMethodField()
    rejected_applications = serializers.SerializerMethodField()

    class Meta:
        model = Freelancer
        fields = [
            "id",
            "user",
            "xrp_address",
            "xrp_seed",
            "how_you_found_us",
            "total_applications",
            "accepted_applications",
            "rejected_applications",
        ]
        extra_kwargs = {"xrp_seed": {"write_only": True}}

    def get_total_applications(self, obj) -> int:
        return getattr(obj, "total_applications", 0)

    def get_accepted_applications(self, obj) -> int:
        return getattr(obj, "accepted_applications", 0)

    def get_rejected_applications(self, obj) -> int:
        return getattr(obj, "rejected_applications", 0)


class CompanyManagerBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyManager
        fields = ["id", "user", "created_at", "updated_at"]


class CompanyValueBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyValue
        fields = [
            "id",
            "name",
        ]


class CompanyIndustryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyIndustry
        fields = [
            "id",
            "name",
        ]


class CompanyBaseSerializer(serializers.ModelSerializer):
    managers = CompanyManagerBaseSerializer(many=True)
    values = CompanyValueBaseSerializer(many=True)
    industry = CompanyIndustryBaseSerializer()
    total_applications = serializers.SerializerMethodField()
    active_jobs = serializers.SerializerMethodField()
    assigned_jobs = serializers.SerializerMethodField()
    completed_jobs = serializers.SerializerMethodField()
    total_jobs = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            "id",
            "user",
            "name",
            "description",
            "email",
            "phone_number",
            "tagline",
            "company_size",
            "organization_type",
            "website",
            "logo",
            "how_you_found_us",
            "xrp_address",
            "managers",
            "values",
            "industry",
            "founded",
            "location",
            "total_jobs",
            "active_jobs",
            "assigned_jobs",
            "completed_jobs",
            "total_applications",
            "created_at",
            "updated_at",
        ]

    def get_total_applications(self, obj) -> int:
        return getattr(obj, "total_applications", 0)

    def get_active_jobs(self, obj) -> int:
        return getattr(obj, "active_jobs", 0)

    def get_total_jobs(self, obj) -> int:
        return getattr(obj, "total_jobs", 0)

    def get_assigned_jobs(self, obj) -> int:
        return getattr(obj, "assigned_jobs", 0)

    def get_completed_jobs(self, obj) -> int:
        return getattr(obj, "completed_jobs", 0)
