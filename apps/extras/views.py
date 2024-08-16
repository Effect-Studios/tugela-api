from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.common.pagination import DefaultPagination
from apps.common.permissions import IsAdmin

from .models import Country, Currency
from .serializers import (
    CountrySerializer,
    CurrencyQueryParamSerializer,
    CurrencySerializer,
)

# Create your views here.

# =================================================================
# ========================= MISCELLANEOUS =========================
# =================================================================
code_param = openapi.Parameter(
    "code",
    openapi.IN_QUERY,
    description="Currency Code",
    type=openapi.TYPE_STRING,
    required=False,
)
type_param = openapi.Parameter(
    "_type",
    openapi.IN_QUERY,
    description=f"Currency Type `{Currency.Type.values}`",
    type=openapi.TYPE_STRING,
    required=False,
)


class MiscellaneousViewSet(ViewSet, DefaultPagination):
    # Countries
    # --------------------------------------------------------------------------
    @swagger_auto_schema(method="GET", responses={200: CountrySerializer})
    @action(detail=False, permission_classes=[AllowAny], methods=["GET"])
    def countries(self, request):
        # countries = [{"name": c[1], "code": c[0]} for c in COUNTRIES]

        qs = Country.objects.all()
        serializer = CountrySerializer(qs, many=True)
        return Response(serializer.data)

        # page = self.paginate_queryset(qs, request)
        # serializer = CountryListSerializer(page, many=True)
        # return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(method="POST", responses={200: CountrySerializer})
    @action(
        detail=False,
        permission_classes=[IsAdmin],
        methods=["POST"],
        url_path="create-country",
    )
    def create_country(self, request):
        serializer = CountrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # TODO: Impelent update country endpoint

    # Currency
    # ----------------------------------------------------------------------------------
    @swagger_auto_schema(
        method="GET",
        manual_parameters=[code_param, type_param],
        responses={200: CurrencySerializer},
    )
    @action(detail=False, permission_classes=[AllowAny], methods=["GET"])
    def currencies(self, request):
        serializer = CurrencyQueryParamSerializer(data=request.query_params)
        serializer.is_valid()
        # currencies = [{"name": c[1], "code": c[0]} for c in Currency.choices]
        qs = Currency.objects.all()
        # filters
        code = serializer.validated_data.get("code")
        _type = serializer.validated_data.get("_type")

        if code:
            qs = qs.filter(code=code)
        if _type:
            qs = qs.filter(_type=_type)

        serializer = CurrencySerializer(qs, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(method="POST", responses={200: CurrencySerializer})
    @action(
        detail=False,
        permission_classes=[IsAdmin],
        methods=["POST"],
        url_path="create-currency",
    )
    def create_currency(self, request):
        serializer = CurrencySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # TODO: implement update currency endpoint

    # Get Ripple balance
    # -----------------------------------------------------------------------------------
    # @swagger_auto_schema(
    #     method="POST",
    #     request_body=,
    #     responses={200: "OK"},
    # )
    # @action(
    #     detail=False,
    #     permission_classes=[AllowAny],
    #     methods=["POST"],
    #     url_path="get-balance",
    # )
    # def get_balance(self, request, *args, **kwargs):
    #  	pass
