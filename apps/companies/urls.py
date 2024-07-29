from rest_framework.routers import SimpleRouter

from .views import CompanyManagerView, CompanyView

router = SimpleRouter()


router.register("company-manager", CompanyManagerView, basename="company-manager")
router.register("", CompanyView, basename="company")


urlpatterns = router.urls
