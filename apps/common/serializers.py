from rest_framework import serializers

from apps.companies.models import Company
from apps.freelancers.models import Freelancer


class FreelancerBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = ["id", "user", "xrp_address", "xrp_seed", "how_you_found_us"]
        extra_kwargs = {"xrp_seed": {"write_only": True}}


class CompanyBaseSerializer(serializers.ModelSerializer):
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
            "xrp_address",
            "created_at",
            "updated_at",
        ]
