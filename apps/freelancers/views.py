import logging

from django.conf import settings
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet

from apps.common.permissions import IsAdmin, IsOwner
from apps.common.xrp import get_account, send_xrp

from .models import Freelancer, PortfolioItem, Service, WorkExperience
from .serializers import (
    FreelancerReadSerializer,
    FreelancerSerializer,
    PortfolioItemMiniSerializer,
    PortfolioItemReadSerializer,
    PortfolioItemSerializer,
    ServiceReadSerializer,
    ServiceSerializer,
    WorkExperienceSerializer,
)


class FreelancerView(ModelViewSet):
    queryset = Freelancer.objects.all().order_by("created_at")
    serializer_class = FreelancerSerializer
    search_fields = ("fullname", "title", "bio", "skills__name")
    filterset_fields = ("user", "gender")
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    http_method_names = [m for m in ModelViewSet.http_method_names if m not in ["put"]]
    ordering = ["created_at"]

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
            self.serializer_class = FreelancerReadSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ["update", "partial_update", "delete"]:
            self.permission_classes = [IsOwner | IsAdmin]
        return super().get_permissions()

    def perform_create(self, serializer):
        # create xrp account
        wallet = get_account("")
        serializer.save(xrp_seed=wallet.seed, xrp_address=wallet.address)

        try:
            # fund account
            if settings.XRP_LIVE:
                xrp_main_seed = settings.XRP_MAIN_SEED
                xrp_amount = 10
                acc_to_fund = wallet.address
                send_xrp(xrp_main_seed, xrp_amount, acc_to_fund)
        except Exception as e:
            logging.warning(e)


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

    def get_serializer_class(self):
        if self.action in ["list"]:
            self.serializer_class = PortfolioItemMiniSerializer
        if self.action in ["retrieve"]:
            self.serializer_class = PortfolioItemReadSerializer
        return super().get_serializer_class()

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
        # return self.queryset.filter(freelancer__user=user)
        return self.queryset

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            self.serializer_class = ServiceReadSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ["update", "partial_update", "delete"]:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        freelancer = serializer.validated_data.get("freelancer")
        serializer.save(user=freelancer.user)
