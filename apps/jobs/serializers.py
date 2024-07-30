from rest_framework import serializers

from .models import Application, Job, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "created_at", "updated_at")


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            "id",
            "title",
            "company",
            "description",
            "date",
            "location",
            "address",
            "tags",
            "price_type",
            "price",
            "currency",
            "application_type",
            "status",
            "external_apply_link",
            "created_at",
            "updated_at",
        )


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("id", "freelancer", "job", "status", "created_at", "updated_at")
