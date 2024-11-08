from django.urls.conf import include, path

app_name = "api"

urlpatterns = [
    path("freelancers/", include("apps.freelancers.urls")),
    path("companies/", include("apps.companies.urls")),
    path("jobs/", include("apps.jobs.urls")),
    path("extras/", include("apps.extras.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("recommendations/", include("apps.recommendations.urls")),
    path("", include("apps.users.urls")),
]
