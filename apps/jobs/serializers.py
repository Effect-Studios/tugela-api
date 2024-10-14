import logging

from django.db import transaction
from rest_framework import serializers

from apps.common.email import send_email_template
from apps.common.serializers import (
    CompanyBaseSerializer,
    FreelancerBaseSerializer,
    JobSubmissionBaseSerializer,
    SkillBaseSerializer,
)
from apps.notifications.utils import fcm_notify

from .models import Application, Job, JobBookmark, JobSubmission, Tag
from .utils import create_escrow, redeem_escrow


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
            "skills",
            "external_apply_link",
            "role_type",
            "responsibilities",
            "experience",
            "max_price",
            "min_price",
            "created_at",
            "updated_at",
        )

    def update(self, instance, validated_data):
        status = validated_data.get("status")
        if (
            status == instance.Status.COMPLETED
            and instance.status == instance.Status.ASSIGNED
        ):
            instance.status = status
            instance.save(update_fields=["status", "updated_at"])

            # redeem escrow
            redeem_escrow(instance)

            return instance

        return super().update(instance, validated_data)


class JobReadSerializer(serializers.ModelSerializer):
    company = CompanyBaseSerializer()
    tags = TagSerializer(many=True)
    skills = SkillBaseSerializer(many=True)

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
            "skills",
            "external_apply_link",
            "role_type",
            "responsibilities",
            "experience",
            "max_price",
            "min_price",
            "escrow_status",
            "created_at",
            "updated_at",
        )


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "id",
            "freelancer",
            "job",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["status"]

    def create(self, validated_data):
        freelancer = validated_data.get("freelancer")

        # check if freelancer has xrp address
        if not freelancer.xrp_address:
            raise serializers.ValidationError({"message": "Update xrp address"})

        return super().create(validated_data)


class CreateEscrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "id",
            "freelancer",
            "status",
            "job",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["freelancer", "job", "status"]

    def save(self):
        data = self.instance
        status = data.status

        if status == Application.Status.ACCEPTED:
            job = data.job
            freelancer = data.freelancer

            # Create Escrow
            return create_escrow(job, freelancer)
        else:
            raise serializers.ValidationError({"message": "Application not accepted"})


class RedeemEscrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "id",
            "freelancer",
            "status",
            "job",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["freelancer", "job", "status"]

    def save(self):
        data = self.instance
        job = data.job

        if job.status == job.Status.COMPLETED:
            # Redeem Escrow
            return redeem_escrow(job)
        else:
            raise serializers.ValidationError({"message": "Escrow condition not met"})


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("id", "freelancer", "job", "status", "created_at", "updated_at")


class ApplicationReadSerializer(serializers.ModelSerializer):
    freelancer = FreelancerBaseSerializer()
    job = JobReadSerializer()
    submission = JobSubmissionBaseSerializer(many=True)

    class Meta:
        model = Application
        fields = (
            "id",
            "freelancer",
            "job",
            "status",
            "submission",
            "created_at",
            "updated_at",
        )


class UpdateApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("id", "freelancer", "job", "status", "created_at", "updated_at")
        read_only_fields = ["freelancer", "job"]

    def update(self, instance, validated_data):
        status = validated_data.get("status")
        if status == instance.Status.ACCEPTED:
            job = instance.job
            if job.status == job.Status.ACTIVE:
                with transaction.atomic():
                    job.status = job.Status.ASSIGNED
                    instance.status = status

                    job.save(update_fields=["status", "updated_at"])
                    instance.save(update_fields=["status", "updated_at"])

                # Create Escrow
                create_escrow(job, instance.freelancer)

                # send in app notification
                title = "Application Approved"
                body = f"Your application for {job.title} at {job.company} has been accepted"
                user = instance.freelancer.user
                fcm_notify(user, title, body)

                try:
                    # send email
                    template_id = "d-1f3bca7a63f74b0c9ed3a72f5a946f54"
                    dynamic_data = {"name": user.username or user.email}
                    send_email_template(
                        user.email, template_id, dynamic_template_data=dynamic_data
                    )
                except Exception as e:
                    logging.warning("Acceptance email failed")
                    logging.warning(e)

                return instance
            else:
                raise serializers.ValidationError({"message": "Job cannot be assigned"})
        return super().update(instance, validated_data)


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobBookmark
        fields = "__all__"


class BookmarkReadSerializer(serializers.ModelSerializer):
    freelancer = FreelancerBaseSerializer()
    job = JobReadSerializer()

    class Meta:
        model = JobBookmark
        fields = "__all__"


class JobSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSubmission
        fields = ["id", "application", "freelancer", "link", "file"]
        extra_kwargs = {"freelancer": {"required": True}}


class JobSubmissionReadSerializer(serializers.ModelSerializer):
    application = ApplicationReadSerializer()
    freelancer = FreelancerBaseSerializer()

    class Meta:
        model = JobSubmission
        fields = ["id", "application", "freelancer", "link", "file"]
