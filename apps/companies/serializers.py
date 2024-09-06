from rest_framework import serializers

from apps.common.serializers import UserBaseSerializer

from .models import Company, CompanyIndustry, CompanyManager, CompanyValue


class CompanyValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyValue
        fields = [
            "id",
            "name",
        ]


class CompanyIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyIndustry
        fields = [
            "id",
            "name",
        ]


class CompanySerializer(serializers.ModelSerializer):
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
            "xrp_seed",
            "values",
            "industry",
            "founded",
            "location",
            "total_jobs",
            "active_jobs",
            "assigned_jobs",
            "completed_jobs",
            "total_applications",
            "visibility",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"user": {"required": True}, "xrp_seed": {"write_only": True}}

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

    # def to_representation(self, instance):
    #     return CompanyBaseSerializer(instance).data


class CompanyManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyManager
        fields = ["id", "user", "company", "created_at", "updated_at"]


class CompanyReadSerializer(serializers.ModelSerializer):
    user = UserBaseSerializer()
    managers = CompanyManagerSerializer(many=True)
    values = CompanyValueSerializer(many=True)
    industry = CompanyIndustrySerializer()
    total_applications = serializers.IntegerField()
    active_jobs = serializers.IntegerField()
    assigned_jobs = serializers.IntegerField()
    completed_jobs = serializers.IntegerField()
    total_jobs = serializers.IntegerField()

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
            "visibility",
            "created_at",
            "updated_at",
        ]

    # def get_total_applications(self, obj) -> int:
    #     return getattr(obj, "total_applications", 0)

    # def get_active_jobs(self, obj) -> int:
    #     return getattr(obj, "active_jobs", 0)

    # def get_total_jobs(self, obj) -> int:
    #     return getattr(obj, "total_jobs", 0)

    # def get_assigned_jobs(self, obj) -> int:
    #     return getattr(obj, "assigned_jobs", 0)

    # def get_completed_jobs(self, obj) -> int:
    #     return getattr(obj, "completed_jobs", 0)
