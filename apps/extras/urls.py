from rest_framework.routers import SimpleRouter

from .views import MiscellaneousViewSet

router = SimpleRouter()
router.register("", MiscellaneousViewSet, basename="misc")


urlpatterns = router.urls
