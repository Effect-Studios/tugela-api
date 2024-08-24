from django.db import transaction
from rest_framework import serializers
from xrpl.utils import xrp_to_drops

from apps.common.models import Currency
from apps.common.serializers import CompanyBaseSerializer, FreelancerBaseSerializer
from apps.common.xrp import (
    create_conditional_escrow,
    finish_conditional_escrow,
    generate_condition,
    get_acc_info,
)

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
            "role_type",
            "responsibilities",
            "experience",
            "max_price",
            "min_price",
            "created_at",
            "updated_at",
        )


class JobReadSerializer(serializers.ModelSerializer):
    company = CompanyBaseSerializer()
    tags = TagSerializer(many=True)

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
            "role_type",
            "responsibilities",
            "experience",
            "max_price",
            "min_price",
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
            raise serializers.ValidationError("Update xrp address")

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
            if job.escrow_sequence and job.escrow_condition and job.escrow_fulfillment:
                raise serializers.ValidationError("Escrow already created")

            company = job.company
            freelancer = data.freelancer

            # check if company has xrp address and seed
            if not company.xrp_address and not company.xrp_seed:
                raise serializers.ValidationError("Update xrp address and seed")

            # check currency
            if job.currency != Currency.XRP:
                raise serializers.ValidationError("Price should be in Ripple")

            # check sufficient balance
            address = company.xrp_address
            price = job.price
            reserve = 15  # ripple accounts must have reserve balance
            price_n_reserve = price + reserve
            price_n_reserve_in_drops = int(xrp_to_drops(price_n_reserve))

            res = get_acc_info(address)
            acc_bal = int(res["Balance"])
            if price_n_reserve_in_drops > acc_bal:
                raise serializers.ValidationError("Insufficient Balance to create job")

            # Create escrow for Job
            condition, fulfillment = generate_condition()
            company_seed = company.xrp_seed
            freelancer_address = freelancer.xrp_address
            finish_time = 60 * 60  # In seconds
            price_in_drops = xrp_to_drops(price)
            escrow = create_conditional_escrow(
                company_seed, price_in_drops, freelancer_address, finish_time, condition
            )
            # Update jobs
            escrow_sequence = escrow["tx_json"]["Sequence"]
            job.escrow_condition = condition
            job.escrow_fulfillment = fulfillment
            job.escrow_sequence = escrow_sequence
            job.save(
                update_fields=[
                    "escrow_sequence",
                    "escrow_condition",
                    "escrow_fulfillment",
                    "updated_at",
                ]
            )

        return {"message": "Escrow created"}


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
            sequence = job.escrow_sequence
            condition = job.escrow_condition
            fulfillment = job.escrow_fulfillment
            if not sequence or not condition or not fulfillment:
                raise serializers.ValidationError("Escrow not created")

            # redeem escrow for Job
            company = job.company
            company_seed = company.xrp_seed
            company_address = company.xrp_address
            finish_conditional_escrow(
                company_seed, company_address, sequence, condition, fulfillment
            )
            return {"message": "Escrow redeemed"}

        return {"message": "Escrow condition not met"}


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("id", "freelancer", "job", "status", "created_at", "updated_at")


class ApplicationReadSerializer(serializers.ModelSerializer):
    freelancer = FreelancerBaseSerializer()
    job = JobReadSerializer()

    class Meta:
        model = Application
        fields = ("id", "freelancer", "job", "status", "created_at", "updated_at")


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

                return instance
        return super().update(instance, validated_data)
