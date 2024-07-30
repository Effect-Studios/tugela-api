from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from apps.common.permissions import IsAdmin, IsCompanyManager, IsCompanyOwner

from .models import Application, Job, Tag
from .serializers import ApplicationSerializer, JobSerializer, TagSerializer


class TagView(ModelViewSet):
    queryset = Tag.objects.all().order_by("created_at")
    serializer_class = TagSerializer
    permission_classes = [IsAdmin]

    http_method_names = [m for m in ModelViewSet.http_method_names if m not in ["put"]]

    def get_permissions(self):
        if self.action in ["list", "read"]:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class JobView(ModelViewSet):
    queryset = Job.objects.all().order_by("created_at")
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "delete"]:
            self.permission_classes = [IsAdmin | IsCompanyOwner | IsCompanyManager]
        return super().get_permissions()


class ApplicationView(ModelViewSet):
    queryset = Application.objects.all().order_by("created_at")
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return self.queryset.none()
        if user.is_staff or user.role == user.Roles.ADMIN:
            return self.queryset
        return self.queryset.filter(
            Q(freelancer__user=user)
            | Q(job__company__in=user.companies_managed)
            | Q(job__company__in=user.company)
        )

    def get_permissions(self):
        if self.action in ["update", "partial_update", "delete"]:
            self.permission_classes = [IsAdmin | IsCompanyOwner | IsCompanyManager]
        return super().get_permissions()
