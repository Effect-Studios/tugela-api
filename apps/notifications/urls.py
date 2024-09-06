from django.urls import include, path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

from .views import NotificationViewSet

router = DefaultRouter()

router.register("fcm-devices", FCMDeviceAuthorizedViewSet)
router.register("", NotificationViewSet, basename="notifications")

urlpatterns = [
    # URLs will show up at <api_root>/devices
    # DRF browsable API which lists all available endpoints
    path("", include(router.urls)),
    # ...
]
