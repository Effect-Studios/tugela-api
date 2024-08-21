from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.companies.models import Company, CompanyManager
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

    class Meta:
        model = Freelancer
        fields = ["id", "user", "xrp_address", "xrp_seed", "how_you_found_us"]
        extra_kwargs = {"xrp_seed": {"write_only": True}}


class CompanyManagerBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyManager
        fields = ["id", "user", "created_at", "updated_at"]


class CompanyBaseSerializer(serializers.ModelSerializer):
    managers = CompanyManagerBaseSerializer(many=True)

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
            "managers",
            "xrp_address",
            "created_at",
            "updated_at",
        ]
