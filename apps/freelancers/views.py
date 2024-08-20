from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet

from apps.common.permissions import IsOwner

from .models import Freelancer, PortfolioItem, Service, WorkExperience
from .serializers import (
    FreelancerSerializer,
    PortfolioItemSerializer,
    ServiceSerializer,
    WorkExperienceSerializer,
)


class FreelancerView(ModelViewSet):
    queryset = Freelancer.objects.all().order_by("created_at")
    serializer_class = FreelancerSerializer
    filterset_fields = ("user",)

    http_method_names = [m for m in ModelViewSet.http_method_names if m not in ["put"]]
    ordering = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return self.queryset.none()
        if user.is_staff or user.role == user.Roles.ADMIN:
            return self.queryset
        return self.queryset.filter(user=user)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "delete"]:
            self.permission_classes = [IsOwner]
        return super().get_permissions()


class WorkExperienceView(ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    filterset_fields = ("user", "freelancer")
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    http_method_names = [m for m in ModelViewSet.http_method_names if m not in ["put"]]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return self.queryset.none()
        if user.is_staff or user.role == user.Roles.ADMIN:
            return self.queryset
        return self.queryset.filter(freelancer__user=user)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "delete"]:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        freelancer = serializer.validated_data.get("freelancer")
        serializer.save(user=freelancer.user)


class PortfolioItemView(ModelViewSet):
    queryset = PortfolioItem.objects.all()
    serializer_class = PortfolioItemSerializer
    filterset_fields = ("user", "freelancer")
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    http_method_names = [m for m in ModelViewSet.http_method_names if m not in ["put"]]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return self.queryset.none()
        if user.is_staff or user.role == user.Roles.ADMIN:
            return self.queryset
        return self.queryset.filter(freelancer__user=user)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "delete"]:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        freelancer = serializer.validated_data.get("freelancer")
        serializer.save(user=freelancer.user)


class ServiceView(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filterset_fields = ("user", "freelancer")
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    http_method_names = [m for m in ModelViewSet.http_method_names if m not in ["put"]]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return self.queryset.none()
        if user.is_staff or user.role == user.Roles.ADMIN:
            return self.queryset
        return self.queryset.filter(freelancer__user=user)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "delete"]:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        freelancer = serializer.validated_data.get("freelancer")
        serializer.save(user=freelancer.user)
