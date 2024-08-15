from rest_framework import serializers

from .models import Freelancer, PortfolioItem, Service, WorkExperience


class FreelancerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = ["id", "user", "xrp_address", "xrp_seed", "how_you_found_us"]
        extra_kwargs = {"xrp_seed": {"write_only": True}}


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
