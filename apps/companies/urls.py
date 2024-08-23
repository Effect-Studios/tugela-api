from rest_framework.routers import SimpleRouter

from .views import (
    CompanyIndustryView,
    CompanyManagerView,
    CompanyValueView,
    CompanyView,
)

router = SimpleRouter()


router.register("managers", CompanyManagerView, basename="company-manager")
router.register("values", CompanyValueView, basename="company-value")
router.register("industries", CompanyIndustryView, basename="company-industry")
router.register("", CompanyView, basename="company")


urlpatterns = router.urls
