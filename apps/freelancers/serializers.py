from rest_framework import serializers

from apps.common.serializers import FreelancerMiniSerializer, UserBaseSerializer
from apps.users.serializers import CategorySerializer, SkillSerializer

from .models import Freelancer, PortfolioItem, Service, WorkExperience


class FreelancerSerializer(serializers.ModelSerializer):
    # total_applications = serializers.SerializerMethodField()
    # accepted_applications = serializers.SerializerMethodField()
    # rejected_applications = serializers.SerializerMethodField()

    class Meta:
        model = Freelancer
        fields = [
            "id",
            "user",
            "title",
            "fullname",
            "bio",
            "location",
            "contact",
            "website",
            "phone_number",
            "profile_image",
            "xrp_address",
            "xrp_seed",
            "skills",
            "visibility",
            "how_you_found_us",
            "total_applications",
            "accepted_applications",
            "rejected_applications",
        ]
        extra_kwargs = {"xrp_seed": {"write_only": True}}

    # def get_total_applications(self, obj) -> int:
    #     return getattr(obj, "total_applications", 0)

    # def get_accepted_applications(self, obj) -> int:
    #     return getattr(obj, "accepted_applications", 0)

    # def get_rejected_applications(self, obj) -> int:
    #     return getattr(obj, "rejected_applications", 0)


class WorkExperienceSerializer(serializers.ModelSerializer):
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


class PortfolioItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioItem
        fields = [
            "id",
            "freelancer",
            "title",
            "description",
            "category",
            "skills",
            "project_url",
            "video_url",
            "start_date",
            "end_date",
            "portfolio_file",
            "created_at",
            "updated_at",
        ]


class PortfolioItemMiniSerializer(serializers.ModelSerializer):
    freelancer = FreelancerMiniSerializer(read_only=True)
    skills = SkillSerializer(many=True)

    class Meta:
        model = PortfolioItem
        fields = [
            "id",
            "freelancer",
            "title",
            "description",
            "category",
            "skills",
            "project_url",
            "video_url",
            "start_date",
            "end_date",
            "portfolio_file",
            "created_at",
            "updated_at",
        ]


class PortfolioItemReadSerializer(serializers.ModelSerializer):
    freelancer = FreelancerMiniSerializer(read_only=True)
    category = CategorySerializer()
    skills = SkillSerializer(many=True)

    class Meta:
        model = PortfolioItem
        fields = [
            "id",
            "freelancer",
            "title",
            "description",
            "category",
            "skills",
            "project_url",
            "video_url",
            "start_date",
            "end_date",
            "portfolio_file",
            "created_at",
            "updated_at",
        ]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "freelancer",
            "title",
            "description",
            "category",
            "skills",
            "delivery_time",
            "starting_price",
            "currency",
            "price_type",
            "service_image",
            "created_at",
            "updated_at",
        ]


class ServiceReadSerializer(serializers.ModelSerializer):
    freelancer = FreelancerMiniSerializer(read_only=True)
    category = CategorySerializer()
    skills = SkillSerializer(many=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "freelancer",
            "title",
            "description",
            "category",
            "skills",
            "delivery_time",
            "starting_price",
            "currency",
            "price_type",
            "service_image",
            "created_at",
            "updated_at",
        ]


class FreelancerReadSerializer(serializers.ModelSerializer):
    user = UserBaseSerializer()
    work_experiences = WorkExperienceSerializer(many=True)
    portfolio_item = PortfolioItemMiniSerializer(many=True)
    services = ServiceSerializer(many=True)
    skills = SkillSerializer(many=True)
    # total_applications = serializers.SerializerMethodField()
    # accepted_applications = serializers.SerializerMethodField()
    # rejected_applications = serializers.SerializerMethodField()

    class Meta:
        model = Freelancer
        fields = [
            "id",
            "user",
            "title",
            "fullname",
            "bio",
            "location",
            "contact",
            "website",
            "phone_number",
            "profile_image",
            "skills",
            "xrp_address",
            "xrp_seed",
            "how_you_found_us",
            "work_experiences",
            "portfolio_item",
            "services",
            "visibility",
            "total_applications",
            "accepted_applications",
            "rejected_applications",
        ]
        extra_kwargs = {"xrp_seed": {"write_only": True}}

    # def get_total_applications(self, obj) -> int:
    #     return obj.total_applications or 0

    # def get_accepted_applications(self, obj) -> int:
    #     return obj.accepted_applications or 0

    # def get_rejected_applications(self, obj) -> int:
    #     return obj.rejected_applications or 0
