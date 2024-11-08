from rest_framework.routers import SimpleRouter

from .views import AIView

router = SimpleRouter()
router.register("", AIView, basename="recommendations")


urlpatterns = router.urls
