from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


def check_auth(request):
    return request.user.is_authenticated


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return check_auth(request) and user.role == User.Roles.USER

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user if check_auth(request) else False


class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return check_auth(request) and user.role == User.Roles.USER

    def has_object_permission(self, request, view, obj):
        return obj.freelancer.user == request.user if check_auth(request) else False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return check_auth(request) and user.role == User.Roles.ADMIN

    def has_object_permission(self, request, view, obj):
        return check_auth(request) and request.user.role == User.Roles.ADMIN


class IsCompanyManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return check_auth(request) and user.role == User.Roles.MANAGER

    def has_object_permission(self, request, view, obj):
        return (
            check_auth(request) and obj.company.mangers in request.user.companies.all()
            if hasattr(obj, "company")
            else obj in request.user.companies.all()
        )


class IsCompanyOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return check_auth(request) and user.role == User.Roles.OWNER

    def has_object_permission(self, request, view, obj):
        return (
            check_auth(request) and obj.company in request.user.company.all()
            if hasattr(obj, "company")
            else obj in request.user.company.all()
        )


class IsTask(BasePermission):
    def has_permission(self, request, view):
        if not settings.GOOGLE_CLOUD_TASKS_ON_GAE or request.META.get(
            "HTTP_X_APPENGINE_QUEUENAME"
        ):
            return True
        return False


class IsCron(BasePermission):
    def has_permission(self, request, view):
        if request.headers.get("X-Appengine-Cron"):
            return True
        return False
