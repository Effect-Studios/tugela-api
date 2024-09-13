from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.companies.models import Company, CompanyIndustry, CompanyManager, CompanyValue
from apps.freelancers.models import Freelancer, PortfolioItem, Service, WorkExperience
from apps.jobs.models import JobSubmission
from apps.users.models import Category, Skill

User = get_user_model()


class SkillBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class CategoryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
        ]


class JobSubmissionBaseSerializer(serializers.ModelSerializer):
    user = UserBaseSerializer()

    class Meta:
        model = JobSubmission
        fields = ["id", "application", "user", "link", "file"]


class WorkExperienceBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = [
            "id",
            "freelancer",
            "job_title",
            "job_description",
            "company_name",
            "currently_working_here",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
        ]


class PortfolioItemBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioItem
        fields = [
            "id",
            "title",
            "description",
            "project_url",
            "video_url",
            "start_date",
            "end_date",
            "portfolio_file",
            "created_at",
            "updated_at",
        ]


class ServiceBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "description",
            "delivery_time",
            "starting_price",
            "currency",
            "price_type",
            "service_image",
            "created_at",
            "updated_at",
        ]


class FreelancerMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = [
            "id",
            "user",
            "fullname",
            "title",
            "bio",
            "location",
            "gender",
            "dob",
            "contact",
            "website",
            "phone_number",
            "profile_image",
        ]


class FreelancerBaseSerializer(serializers.ModelSerializer):
    user = UserBaseSerializer()
    skills = SkillBaseSerializer(many=True)
    work_experiences = WorkExperienceBaseSerializer(many=True)
    portfolio_item = PortfolioItemBaseSerializer(many=True)
    services = ServiceBaseSerializer(many=True)
    # total_applications = serializers.SerializerMethodField()
    # accepted_applications = serializers.SerializerMethodField()
    # rejected_applications = serializers.SerializerMethodField()

    class Meta:
        model = Freelancer
        fields = [
            "id",
            "user",
            "fullname",
            "title",
            "bio",
            "location",
            "gender",
            "dob",
            "contact",
            "website",
            "phone_number",
            "profile_image",
            "skills",
            "work_experiences",
            "portfolio_item",
            "services",
            "visibility",
            "xrp_address",
            "xrp_seed",
            "how_you_found_us",
            "total_applications",
            "accepted_applications",
            "rejected_applications",
        ]
        extra_kwargs = {"xrp_seed": {"write_only": True}}

    # def get_total_applications(self, obj) -> int:
    #     print("debug: ", vars(obj))
    #     return getattr(obj, "total_applications", 0)

    # def get_accepted_applications(self, obj) -> int:
    #     return getattr(obj, "accepted_applications", 0)

    # def get_rejected_applications(self, obj) -> int:
    #     return getattr(obj, "rejected_applications", 0)


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
            "visibility",
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
