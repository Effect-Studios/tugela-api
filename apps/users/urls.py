from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    AddressView,
    CategoryView,
    ChangePasswordView,
    ForgotPasswordView,
    ProfileView,
    ResetPasswordView,
    SignUpView,
    SkillView,
    UserView,
)

router = DefaultRouter()

router.register("users", UserView, basename="users")
router.register("profile", ProfileView, basename="profile")
router.register("address", AddressView, basename="address")
router.register("category", CategoryView, basename="category")
router.register("skills", SkillView, basename="skill")


urlpatterns = [
    path("auth/signup/", SignUpView.as_view(), name="signup"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("auth/refresh-token/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/forget-password/", ForgotPasswordView.as_view(), name="forget-password"),
    path("auth/reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("", include(router.urls)),
]
