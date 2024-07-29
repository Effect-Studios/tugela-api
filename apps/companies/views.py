from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet

from apps.common.permissions import IsAdmin, IsOwner

from .models import Company, CompanyManager
from .serializers import CompanyManagerSerializer, CompanySerializer


class CompanyView(ModelViewSet):
    queryset = Company.objects.all().order_by("created_at")
    serializer_class = CompanySerializer
    filterset_fields = ("user", "company_size", "organization_type")
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    http_method_names = [m for m in ModelViewSet.http_method_names if m not in ["put"]]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return self.queryset.none()
        if user.is_staff or user.role == user.Roles.ADMIN:
            return self.queryset
        return self.queryset.filter(user=user)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "delete"]:
            self.permission_classes = [IsOwner | IsAdmin]
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
        return self.queryset.filter(user=user)
