from rest_framework.routers import SimpleRouter

from .views import ApplicationView, BookmarkView, JobView, TagView

router = SimpleRouter()


router.register("applications", ApplicationView, basename="applications")
router.register("tags", TagView, basename="tags")
router.register("bookmarks", BookmarkView, basename="bookmarks")
router.register("", JobView, basename="jobs")


urlpatterns = router.urls
