from rest_framework import serializers

from .models import Company, CompanyManager


class CompanySerializer(serializers.ModelSerializer):
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
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"user": {"required": True}, "xrp_seed": {"write_only": True}}


class CompanyManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyManager
        fields = ["id", "user", "company", "created_at", "updated_at"]
