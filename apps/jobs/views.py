from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.common.permissions import IsAdmin, IsCompanyManager, IsCompanyOwner

from .models import Application, Job, JobBookmark, Tag
from .serializers import (
    ApplicationCreateSerializer,
    ApplicationReadSerializer,
    ApplicationSerializer,
    BookmarkReadSerializer,
    BookmarkSerializer,
    CreateEscrowSerializer,
    JobReadSerializer,
    JobSerializer,
    RedeemEscrowSerializer,
    TagSerializer,
    UpdateApplicationStatusSerializer,
)

# api schema
response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
)


class TagView(ModelViewSet):
    queryset = Tag.objects.all().order_by("created_at")
    serializer_class = TagSerializer
    permission_classes = [IsAdmin]

    http_method_names = [m for m in ModelViewSet.http_method_names if m not in ["put"]]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class JobView(ModelViewSet):
    queryset = Job.objects.all().order_by("created_at")
    serializer_class = JobSerializer
    filterset_fields = ("company",)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "delete"]:
            self.permission_classes = [IsAdmin | IsCompanyOwner | IsCompanyManager]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            self.serializer_class = JobReadSerializer
        return super().get_serializer_class()


class ApplicationView(ModelViewSet):
    queryset = Application.objects.all().order_by("created_at")
    serializer_class = ApplicationSerializer
    filterset_fields = ("freelancer", "job", "status")

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return self.queryset.none()
        if user.is_staff or user.role == user.Roles.ADMIN:
            return self.queryset
        return self.queryset.filter(
            Q(freelancer__user=user)
            | Q(job__company__managers__in=user.companies_managed.all())
            | Q(job__company__user=user)
        )

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = ApplicationCreateSerializer
        if self.action in ["retrieve", "list"]:
            self.serializer_class = ApplicationReadSerializer
        if self.action == "create_escrow":
            self.serializer_class = CreateEscrowSerializer
        if self.action == "redeem_escrow":
            self.serializer_class = RedeemEscrowSerializer
        if self.action == "update_status":
            self.serializer_class = UpdateApplicationStatusSerializer
        return super().get_serializer_class()

    # def get_permissions(self):
    #     if self.action in ["update", "partial_update", "delete"]:
    #         self.permission_classes = [IsAdmin | IsCompanyOwner | IsCompanyManager]
    #     return super().get_permissions()

    @swagger_auto_schema(
        method="get",
        # request_body=CreateEscrowSerializer,
        responses={200: response_schema},
    )
    @action(detail=True, methods=["GET"], url_path="create-escrow")
    def create_escrow(self, request, *args, **kwargs):
        application = self.get_object()
        serializer = self.get_serializer(application)
        res = serializer.save()
        return Response(res, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="get",
        # request_body=CreateEscrowSerializer,
        responses={200: response_schema},
    )
    @action(detail=True, methods=["GET"], url_path="redeem-escrow")
    def redeem_escrow(self, request, *args, **kwargs):
        application = self.get_object()
        serializer = self.get_serializer(application)
        res = serializer.save()
        return Response(res, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        request_body=UpdateApplicationStatusSerializer,
        responses={200: response_schema},
    )
    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAdmin | IsCompanyOwner | IsCompanyManager],
        url_path="update-status",
    )
    def update_status(self, request, *args, **kwargs):
        application = self.get_object()
        serializer = self.get_serializer(application, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookmarkView(ModelViewSet):
    queryset = JobBookmark.objects.all().order_by("created_at")
    serializer_class = BookmarkSerializer
    filterset_fields = ("freelancer", "job")

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return self.queryset.none()
        if user.is_staff or user.role == user.Roles.ADMIN:
            return self.queryset
        return self.queryset.filter(freelancer__user=user)

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            self.serializer_class = BookmarkReadSerializer
        return super().get_serializer_class()
