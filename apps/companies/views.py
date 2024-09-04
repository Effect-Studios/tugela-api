from django.db.models import Q
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from apps.common.permissions import IsAdmin, IsCompanyOwner

from .models import Company, CompanyIndustry, CompanyManager, CompanyValue
from .serializers import (
    CompanyIndustrySerializer,
    CompanyManagerSerializer,
    CompanyReadSerializer,
    CompanySerializer,
    CompanyValueSerializer,
)


class CompanyView(ModelViewSet):
    queryset = Company.objects.all().order_by("created_at")
    serializer_class = CompanySerializer
    search_fields = ("name", "description", "email")
    filterset_fields = ("user", "company_size", "organization_type")
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    http_method_names = [m for m in ModelViewSet.http_method_names if m not in ["put"]]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return self.queryset.none()
        if user.is_staff or user.role == user.Roles.ADMIN:
            return self.queryset
        # return self.queryset.filter(user=user)
        return self.queryset

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            self.serializer_class = CompanyReadSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ["update", "partial_update", "delete"]:
            self.permission_classes = [IsCompanyOwner | IsAdmin]
        return super().get_permissions()


class CompanyManagerView(ModelViewSet):
    queryset = CompanyManager.objects.all().order_by("created_at")
    serializer_class = CompanyManagerSerializer
    filterset_fields = ("user", "company")

    http_method_names = [
        m for m in ModelViewSet.http_method_names if m not in ["put", "patch"]
    ]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return self.queryset.none()
        if user.is_staff or user.role == user.Roles.ADMIN:
            return self.queryset
        return self.queryset.filter(Q(user=user) | Q(company__user=user))


class CompanyValueView(ReadOnlyModelViewSet):
    queryset = CompanyValue.objects.all().order_by("created_at")
    serializer_class = CompanyValueSerializer
    permission_classes = [AllowAny]


class CompanyIndustryView(ReadOnlyModelViewSet):
    queryset = CompanyIndustry.objects.all().order_by("created_at")
    serializer_class = CompanyIndustrySerializer
    permission_classes = [AllowAny]
