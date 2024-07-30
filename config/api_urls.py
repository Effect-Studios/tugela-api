from django.urls.conf import include, path

app_name = "api"

urlpatterns = [
    path("freelancers/", include("apps.freelancers.urls")),
    path("companies/", include("apps.companies.urls")),
    path("jobs/", include("apps.jobs.urls")),
    path("", include("apps.users.urls")),
]
