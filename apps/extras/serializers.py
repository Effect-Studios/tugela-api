from rest_framework import serializers
from xrpl.utils import drops_to_xrp

from apps.common.xrp import get_acc_info

from .models import Country, Currency


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
