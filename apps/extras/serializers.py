from rest_framework import serializers

from .models import Country, Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("uuid", "code", "name", "factor", "precision", "symbol", "_type")


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["uuid", "name", "iso", "code"]


class CurrencyQueryParamSerializer(serializers.Serializer):
    def get_currency_types():
        return Currency.Type.choices

    code = serializers.CharField(required=False)
    _type = serializers.ChoiceField(choices=get_currency_types(), required=False)
