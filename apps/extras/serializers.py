import logging

from rest_framework import serializers
from xrpl.utils import drops_to_xrp

from apps.common.xrp import get_acc_info, send_xrp
from apps.companies.models import Company
from apps.freelancers.models import Freelancer

from .models import Country, Currency, PaymentService


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "code", "name", "factor", "precision", "symbol", "_type")


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "iso", "code"]


class CurrencyQueryParamSerializer(serializers.Serializer):
    def get_currency_types():
        return Currency.Type.choices

    code = serializers.CharField(required=False)
    _type = serializers.ChoiceField(choices=get_currency_types(), required=False)


class XRPBalanceSerializer(serializers.Serializer):
    xrp_address = serializers.CharField(write_only=True)
    account = serializers.CharField(read_only=True)
    xrp_balance = serializers.DecimalField(
        max_digits=14, decimal_places=2, read_only=True
    )

    def save(self):
        addr = self.validated_data.get("xrp_address")
        try:
            res = get_acc_info(addr)
            drops = res.get("Balance")
            if drops:
                res["xrp_balance"] = drops_to_xrp(drops)
            return res
        except Exception as e:
            raise serializers.ValidationError({"message": e})


class XRPWithdrawalSerializer(serializers.Serializer):
    xrp_address = serializers.CharField(required=True)
    xrp_amount = serializers.DecimalField(
        max_digits=14, decimal_places=2, required=True
    )
    freelancer = serializers.PrimaryKeyRelatedField(
        queryset=Freelancer.objects.all(), required=False
    )
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), required=False
    )

    def validate(self, obj):
        validated_data = super().validate(obj)

        company = validated_data.get("company")
        freelancer = validated_data.get("freelancer")

        if freelancer and company:
            raise serializers.ValidationError(
                {"message": "Provide only one company or freelancer"}
            )

        if not freelancer and not company:
            raise serializers.ValidationError(
                {"message": "Provide only one company or freelancer"}
            )

        return validated_data

    def save(self):
        addr = self.validated_data.get("xrp_address")
        amount = self.validated_data.get("xrp_amount")
        company = self.validated_data.get("company")
        freelancer = self.validated_data.get("freelancer")

        request = self.context.get("request")
        user = request.user
        from_seed = None

        if company:
            # check if user is authorised
            if company.user != user:
                raise serializers.ValidationError(
                    {"message": "Not authorised to perform action"}
                )

            from_seed = company.xrp_seed

        if freelancer:
            # check if user is authorised
            if freelancer.user != user:
                raise serializers.ValidationError(
                    {"message": "Not authorised to perform action"}
                )

            from_seed = freelancer.xrp_seed

        if not from_seed:
            raise serializers.ValidationError({"message": "No xrp to transfer"})

        try:
            _ = send_xrp(from_seed, amount, addr)
        except Exception as e:
            logging.warning(e)
            raise serializers.ValidationError(
                {"message": "XRP transfer failed", "error": e}
            )

        return {"message": "Transfer Successful"}


class PaymentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentService
        fields = ["id", "name", "url", "status"]
