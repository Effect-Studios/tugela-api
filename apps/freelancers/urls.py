from rest_framework.routers import SimpleRouter

from .views import FreelancerView, PortfolioItemView, ServiceView, WorkExperienceView

router = SimpleRouter()


router.register("work-experiences", WorkExperienceView, basename="work-experiences")
router.register("portfolio-items", PortfolioItemView, basename="portfolio-items")
router.register("services", ServiceView, basename="services")
router.register("", FreelancerView, basename="freelancers")


urlpatterns = router.urls
