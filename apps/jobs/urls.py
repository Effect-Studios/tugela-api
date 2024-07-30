from rest_framework.routers import SimpleRouter

from .views import ApplicationView, JobView, TagView

router = SimpleRouter()


router.register("applications", ApplicationView, basename="applications")
router.register("tags", TagView, basename="tags")
router.register("", JobView, basename="jobs")


urlpatterns = router.urls
